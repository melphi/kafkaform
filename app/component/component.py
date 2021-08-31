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

    def as_entry(self, spec: model.SpecItem) -> dict:
        entry = {"name": spec.name}
        entry.update(spec.params)
        if spec.schema_name:
            entry["schema_name"] = spec.schema_name
        return entry


class Resolver:
    """Resolves resources current state"""

    def describe(self, target: model.SpecItem) -> model.Description:
        raise NotImplementedError()

    def equals(self, current: model.SpecItem, target: model.SpecItem) -> bool:
        raise NotImplementedError()

    def system_list(self) -> List[str]:
        raise NotImplementedError()

    def system_get(self, name: str) -> Optional[model.SpecItem]:
        raise NotImplementedError()


class Transitioner:
    """Performs state transitions."""

    def apply(self, delta: model.DeltaItem) -> None:
        raise NotImplementedError()

    def drop(self, spec: model.SpecItem, *, cascade: bool = False) -> None:
        raise NotImplementedError()

    def validate(self, delta: model.DeltaItem) -> None:
        raise NotImplementedError()


@dataclass
class Component:
    resource_type: str
    parser: Optional[Parser]
    resolver: Resolver
    transitioner: Optional[Transitioner]
