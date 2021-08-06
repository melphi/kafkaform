import dataclasses
from typing import Dict, IO, Iterator, List

import os
import jinja2
import jsonschema
import yaml

from app import model
from app.component import component


class Parser:
    def __init__(self, *, parsers_map: Dict[str, component.Parser]):
        self._parsers_by_type = parsers_map
        self._parsers_by_tag = {parser.tag_name(): parser for parser in parsers_map.values()}

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
        Parses the definitions file. Supports Jinja2 template tags.
        """

        try:
            content = self.render(file_name)
            docs = yaml.safe_load_all(content)
            doc = self._merge_docs(docs)
            self._check_schema(doc)
            return self._build_spec(doc)
        except Exception as e:
            raise ValueError(f"Error while parsing file [{file_name}]: {str(e)}")

    def save(self, *, data: model.Spec, target: IO) -> None:
        """
        Saves the model into a definition file.
        """

        values: Dict[str, List] = {}
        for spec in data.specs:
            parser = self._parsers_by_type.get(spec.resource_type)
            if parser:
                entry = parser.as_entry(spec)
                if parser.tag_name() in values:
                    values[parser.tag_name()].append(entry)
                else:
                    values[parser.tag_name()] = [entry]
        yaml.safe_dump(values, target)

    def _merge_docs(self, docs: Iterator[dict]) -> dict:
        res = {}
        for doc in docs:
            for key, val in doc.items():
                if key in res:
                    if val is None:
                        continue
                    elif res[key] is None:
                        res[key] = val
                    elif isinstance(val, list) and isinstance(res[key], list):
                        res[key].extend(val)
                    elif isinstance(val, dict) and isinstance(res[key], dict):
                        repeated = set(val.keys()).intersection(res[key].keys())
                        assert len(repeated) == 0, \
                            f"Entry [{key}] is a dict, it can not contain repeated sub entries [{repeated}]."
                        res[key].update(val)
                    else:
                        raise ValueError(f"Entry [{key}] is repeated with different or not updatable data types, "
                                         f"eg. lists or dictionaries.")
                else:
                    res[key] = val
        return res

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
            parser = self._parsers_by_tag.get(key)
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
        for name, parser in self._parsers_by_type.items():
            schema = parser.schema()
            assert schema, f"Parser [{name}] did not return any schema."
            schemas[name] = schema
        return {
            "type": "object",
            "properties": schemas}
