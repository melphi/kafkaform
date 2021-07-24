from typing import Dict, List

import os
import jinja2
import jsonschema
import yaml

from app import model
from app.component import component


# TODO: Parse repeated tags.
class Parser:
    def __init__(self, parsers: List[component.Parser]):
        self._parsers_map: Dict[str, component.Parser] = {parser.tag_name(): parser for parser in parsers}

    def render(self, file_path: str) -> str:
        """Renders jinja2 template file into a string"""

        path = os.path.dirname(file_path)
        file = os.path.basename(file_path)
        if not file:
            raise ValueError(f"Path {file_path} requires a file name")
        engine = jinja2.Environment(loader=jinja2.FileSystemLoader(path),
                                    undefined=jinja2.StrictUndefined)
        try:
            return engine.get_template(file).render()
        except jinja2.TemplateNotFound as e:
            raise ValueError(f"Template file not found: {e.message}")
        except jinja2.exceptions.TemplateAssertionError as e:
            raise ValueError(f"Template render error in file {e.filename}, line {e.lineno}: {e.message}")
        except jinja2.exceptions.TemplateSyntaxError as e:
            raise ValueError(f"Template render error in file {e.filename}, line {e.lineno}: {e.message}")
        except jinja2.exceptions.UndefinedError as e:
            raise ValueError(f"Unresolved element: {e.message}")

    def parse(self, file_name: str) -> model.Spec:
        """
        Parses the file name into a specification object.
        Supports Jinja2 template format for input files.
        """

        try:
            content = self.render(file_name)
            doc = yaml.safe_load(content)
            self._check_schema(doc)
            return self._build_spec(doc)
        except Exception as e:
            raise ValueError(f"Error while parsing file [{file_name}]: {str(e)}")

    def _check_schema(self, doc: dict) -> None:
        self._check_no_empty_spec(doc)
        schema = self._build_schema()
        try:
            jsonschema.validate(doc, schema)
        except jsonschema.ValidationError as e:
            path = "/".join([str(item) for item in e.path])
            raise ValueError(f"File format is not valid in path [{path}]: error {e.message}")

    def _build_spec(self, doc: dict) -> model.Spec:
        specs = list()
        for key, val in doc.items():
            parser = self._parsers_map.get(key)
            assert parser, f"Tag {key} does not have any registered parser"
            for spec in parser.parse(val):
                specs.append(spec)
        return model.Spec(specs=specs)

    def _check_no_empty_spec(self, doc: dict) -> None:
        for key, val in doc.items():
            if val:
                return
        raise ValueError("Configuration does not define any resource")

    def _build_schema(self) -> dict:
        schemas = {}
        for name, parser in self._parsers_map.items():
            schema = parser.schema()
            assert schema, f"Parser [{name}] did not return any schema."
            schemas[name] = schema
        return {
            "type": "object",
            "properties": schemas
        }
