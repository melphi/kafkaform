from typing import List, Optional
from dataclasses import dataclass

from app.model import spec


RESOURCE_CONNECTOR_CLASS = "connector_class"
RESOURCE_QUERY = "query"
RESOURCE_SCHEMA = "schema"
RESOURCE_SINK = "sink"
RESOURCE_SOURCE = "source"
RESOURCE_STREAM = "stream"
RESOURCE_TABLE = "table"
RESOURCE_TOPIC = "topic"
RESOURCE_UDF = "udf"


@dataclass
class ConnectParams:
    config: dict


@dataclass
class Dependency:
    name: str
    resource_type: str


@dataclass
class StreamParams:
    sql: str


@dataclass
class TableParams:
    sql: str


@dataclass
class TopicParams:
    partitions: int
    replicas: int


@dataclass
class FieldSchema:
    name: str
    type: str


@dataclass
class SchemaParams:
    fields: List[FieldSchema]


@dataclass
class Description:
    depends: List[Dependency]
    schema: Optional[SchemaParams]
    spec: spec.SpecItem
