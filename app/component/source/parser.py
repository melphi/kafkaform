import dataclasses

from app.component import component
from app import model


class SourceParser(component.Parser):
    def tag_name(self) -> str:
        return "sources"

    def schema(self) -> dict:
        return {
            "sources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "config": {"type": "object"},
                        "schema": {"type": "string"}
                    },
                    "additionalProperties": False,
                    "required": ["name", "config"]
                }
            }
        }

    def parse(self, item: dict) -> model.SpecItem:
        params = model.ConnectParams(config=item.get("config"))
        return model.SpecItem(
            name=item.get("name"),
            resource_type=model.RESOURCE_SOURCE,
            params=dataclasses.asdict(params),
            schema_name=item.get("schema"))