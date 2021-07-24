from typing import List
import dataclasses

from app.component import component
from app import model


class SinkParser(component.Parser):
    def tag_name(self) -> str:
        return "sinks"

    def schema(self) -> dict:
        return {
            "sinks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "config": {"type": "object"}
                    },
                    "additionalProperties": False,
                    "required": ["name", "config"]
                }
            }
        }

    def parse(self, block: dict) -> List[model.SpecItem]:
        specs = list()
        for item in block[self.tag_name()]:
            params = model.ConnectParams(config=item.get("config"))
            specs.append(model.SpecItem(
                name=item.get("name"),
                resource_type=model.RESOURCE_SINK,
                params=dataclasses.asdict(params),
                schema_name=None))
        return specs
