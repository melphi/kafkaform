from typing import List
import dataclasses

from app.component import component
from app import model


class TableParser(component.Parser):
    def tag_name(self) -> str:
        return "tables"

    def schema(self) -> dict:
        return {
            "tables": {
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

    def parse(self, block: dict) -> List[model.SpecItem]:
        specs = list()
        for item in block[self.tag_name()]:
            params = model.StreamParams(sql=item.get("sql"))
            specs.append(model.SpecItem(
                name=item.get("name"),
                params=dataclasses.asdict(params),
                resource_type=model.RESOURCE_TABLE,
                schema_name=item.get("schema")))
        return specs
