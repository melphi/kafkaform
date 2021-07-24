from dataclasses import dataclass
from typing import List, Optional

from app.model import spec


@dataclass
class DeltaItem:
    resource_type: str
    deleted: bool
    current: Optional[spec.SpecItem]
    target: Optional[spec.SpecItem]


@dataclass
class Delta:
    items: List[DeltaItem]


EMPTY_DELTA = Delta(items=list())
