from typing import Optional, List

from app import model
from app.component import component


class UdfResolver(component.Resolver):
    def describe(self, target: model.SpecItem) -> model.Description:
        raise NotImplementedError()

    def system_list(self) -> List[str]:
        raise NotImplementedError()

    def system_get(self, name: str) -> Optional[model.SpecItem]:
        raise NotImplementedError()
