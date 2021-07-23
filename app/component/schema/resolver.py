from typing import List, Optional

from app import model
from app.component import component


class SchemaResolver(component.Resolver):
    def describe(self, target: model.SpecItem) -> model.Description:
        schema = model.SchemaParams(**target.params)
        return model.Description(
            depends=list(),
            spec=target,
            schema=schema)

    def system_list(self) -> List[str]:
        # TODO: Load schema from Informatica EDC.
        return []

    def system_get(self, name: str) -> Optional[model.SpecItem]:
        # TODO: Load schema from Informatica EDC.
        return None
