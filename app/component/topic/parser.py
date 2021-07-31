import dataclasses
from typing import List

from app import component, model


class TopicParser(component.Parser):
    def tag_name(self) -> str:
        return "topics"

    def schema(self) -> dict:
        return {
            "tables": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "partitions": {"type": "integer"},
                        "replicas": {"type": "integer"},
                        "schema": {"type": "string"},
                    },
                    "additionalProperties": False,
                    "required": ["name"]
                }
            }
        }

    def parse(self, block: dict) -> List[model.SpecItem]:
        assert isinstance(block, list)
        specs = list()
        for item in block:
            params = model.TopicParams(
                partitions=item.get("partitions"),
                replicas=item.get("replicas"))
            specs.append(model.SpecItem(
                name=item.get("name"),
                params=dataclasses.asdict(params),
                resource_type=model.RESOURCE_TOPIC,
                schema_name=item.get("schema_name")))
        return specs

