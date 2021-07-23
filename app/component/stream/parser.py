import dataclasses

from app.component import component
from app import model


class StreamParser(component.Parser):
    def tag_name(self) -> str:
        return "streams"

    def schema(self) -> dict:
        return {
            "streams": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "sql": {"type": "string"},
                        "schema": {"type": "string"}
                    },
                    "additionalProperties": False,
                    "required": ["name", "sql"]
                }
            }
        }

    def parse(self, item: dict) -> model.SpecItem:
        params = model.StreamParams(sql=item.get("sql"))
        return model.SpecItem(
            name=item.get("name"),
            params=dataclasses.asdict(params),
            resource_type=model.RESOURCE_STREAM,
            schema_name=item.get("schema"))
