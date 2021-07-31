from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ConnectorInfo:
    name: str
    config: Dict[str, str]
    tasks: List[Dict[str, str]]


@dataclass
class ResourceInfo:
    name: str
    sql: str


@dataclass
class TopicInfo:
    name: str
    partitions: int
    replicas: int


@dataclass
class UdfFunctionInfo:
    return_type: str


@dataclass
class UdfInfo:
    name: str
    functions: List[UdfFunctionInfo]
