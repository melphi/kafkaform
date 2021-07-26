from dataclasses import dataclass
from typing import List, Optional

from app import model


class Parser:
    """Parsers specification files"""

    def tag_name(self) -> str:
        raise NotImplementedError()

    def schema(self) -> dict:
        raise NotImplementedError()

    def parse(self, block: dict) -> List[model.SpecItem]:
        raise NotImplementedError()


class Resolver:
    """Resolves resources current state"""

    def describe(self, target: model.SpecItem) -> model.Description:
        raise NotImplementedError()

    def equals(self, current: model.SpecItem, target: model.SpecItem) -> bool:
        assert current.resource_type == target.resource_type, \
            f"Can not compare resource type [{current.resource_type}] with [{current.resource_type}]"
        return current.name == target.name and current.params == target.params

    def system_list(self) -> List[str]:
        raise NotImplementedError()

    def system_get(self, name: str) -> Optional[model.SpecItem]:
        raise NotImplementedError()


class Transitioner:
    """Performs state transitions."""

    def apply(self, delta: model.DeltaItem) -> None:
        raise NotImplementedError()


@dataclass
class Component:
    resource_type: str
    parser: Optional[Parser]
    resolver: Resolver
    transitioner: Optional[Transitioner]
