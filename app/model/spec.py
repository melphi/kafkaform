import enum
from dataclasses import dataclass
from typing import List, Optional


class FieldType(enum.Enum):
    """Supported field types"""

    BIGINT = "BIGINT"
    BOOLEAN = "BOOLEAN"
    DECIMAL = "DECIMAL"
    DOUBLE = "DOUBLE"
    INT = "INT"
    STRING = "STRING"
    TIMESTAMP = "TIMESTAMP"
    VARCHAR = "VARCHAR"


@dataclass
class SpecItem:
    """Specification item"""

    name: str
    resource_type: str
    params: dict
    schema_name: Optional[str]

    def full_name(self):
        """Returns the fully qualified name of the resource"""

        return f"{self.resource_type}:{self.name}"


@dataclass
class Spec:
    """Complete specification"""

    specs: List[SpecItem]


EMPTY_SPEC = Spec(specs=list())
