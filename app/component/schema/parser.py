from typing import List
import dataclasses

from app.component import component
from app import model


class SchemaParser(component.Parser):
    def tag_name(self) -> str:
        return "schemas"

    def schema(self) -> dict:
        return {
            "schemas": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "fields": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"type": "string"}
                                },
                                "additionalProperties": False,
                                "required": ["name", "type"]
                            }
                        }
                    },
                    "additionalProperties": False,
                    "required": ["name", "fields"]
                }
            }
        }

    def parse(self, block: dict) -> List[model.SpecItem]:
        assert isinstance(block, list)
        specs = list()
        for item in block:
            fields = list()
            if item.get("fields"):
                assert isinstance(item["fields"], list), "Fields should be a list of values"
                for field in item["fields"]:
                    fields.append(model.FieldSchema(
                        name=field.get("name"),
                        type=field.get("type")))
            params = model.SchemaParams(fields=fields)
            specs.append(model.SpecItem(
                name=item.get("name"),
                schema_name=item.get("name"),
                resource_type=model.RESOURCE_SCHEMA,
                params=dataclasses.asdict(params)))
        return specs

    def _parse_type(self, type_name: str) -> model.FieldType:
        assert type_name, "Missing field type value"
        try:
            return model.FieldType(type_name.upper())
        except Exception:
            raise ValueError(f"Unsupported field type [{type_name.upper()}], "
                             f"allowed types [{list(model.FieldType)}]")
