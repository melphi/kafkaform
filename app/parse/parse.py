from typing import IO

import dataclasses
import jinja2
import yaml
import os

from app import model
from app.parse import schema


class Parser:
    """Parses the resources definition file."""

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
            schema.validate(doc)

            res = model.Spec(
                schemas=list(),
                sinks=list(),
                sources=list(),
                streams=list(),
                tables=list())
            for key, val in doc.items():
                if val:
                    if key == "schemas":
                        for item in val:
                            res.schemas.append(self._parse_schema(item))
                    elif key == "sinks":
                        for item in val:
                            res.sinks.append(self._parse_sink(item))
                    elif key == "sources":
                        for item in val:
                            res.sources.append(self._parse_source(item))
                    elif key == "streams":
                        for item in val:
                            res.streams.append(self._parse_stream(item))
                    elif key == "tables":
                        for item in val:
                            res.tables.append(self._parse_table(item))
                    else:
                        raise ValueError(f"Unsupported key [{key}]")
            return res
        except Exception as e:
            raise ValueError(f"Error while parsing file [{file_name}]: {str(e)}")

    def save(self, *, data: model.Spec, target: IO) -> None:
        values = dataclasses.asdict(data)
        yaml.safe_dump(values, target)

    def _parse_schema(self, val: dict) -> model.SchemaSpec:
        fields = list()
        if val.get("fields"):
            assert isinstance(val["fields"], list), "Fields should be a list of values"
            for field in val["fields"]:
                fields.append(model.FieldSpec(
                    name=field.get("name"),
                    type=self._parse_type(field.get("type"))))
        return model.SchemaSpec(
            name=val.get("name"),
            fields=fields)

    def _parse_type(self, type_name: str) -> model.FieldType:
        assert type_name, "Missing field type value"
        try:
            return model.FieldType(type_name.upper())
        except Exception:
            raise ValueError(f"Unsupported field type [{type_name.upper()}], "
                             f"allowed types [{list(model.FieldType)}]")

    def _parse_sink(self, val: dict) -> model.SinkSpec:
        return model.SinkSpec(name=val.get("name"))

    def _parse_source(self, val: dict) -> model.SourceSpec:
        return model.SourceSpec(
            name=val.get("name"),
            config=val.get("config"),
            schema=model.SchemaSpec(name=val.get("schema"), fields=list()))

    def _parse_stream(self, val: dict) -> model.StreamSpec:
        return model.StreamSpec(
            name=val.get("name"),
            sql=val.get("sql"),
            schema=model.SchemaSpec(name=val.get("schema"), fields=list()))

    def _parse_table(self, val: dict) -> model.TableSpec:
        return model.TableSpec(
            name=val.get("name"),
            sql=val.get("sql"),
            schema=model.SchemaSpec(name=val.get("schema"), fields=list()))


PARSER = Parser()
