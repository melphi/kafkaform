from typing import List

from app import client, model
from app.component import component, schema, sink, source, stream, table


def build_all(*,
              connect_client: client.ConnectClient,
              ksql_client: client.KsqlClient) -> List[component.Component]:
    components = list()

    # Schema
    components.append(component.Component(
        resource_type=model.RESOURCE_SCHEMA,
        parser=schema.SchemaParser(),
        resolver=schema.SchemaResolver(),
        transitioner=None))

    # Sink
    components.append(component.Component(
        resource_type=model.RESOURCE_SINK,
        parser=sink.SinkParser(),
        resolver=sink.SinkResolver(connect_client=connect_client),
        transitioner=sink.SinkTransitioner(connect_client=connect_client)))

    # Source
    components.append(component.Component(
        resource_type=model.RESOURCE_SOURCE,
        parser=source.SourceParser(),
        resolver=source.SourceResolver(connect_client=connect_client),
        transitioner=source.SourceTransitioner(connect_client=connect_client)))

    # Stream
    components.append(component.Component(
        resource_type=model.RESOURCE_STREAM,
        parser=stream.StreamParser(),
        resolver=stream.StreamResolver(ksql_client=ksql_client),
        transitioner=stream.StreamTransitioner(ksql_client=ksql_client)))

    # Table
    components.append(component.Component(
        resource_type=model.RESOURCE_TABLE,
        parser=table.TableParser(),
        resolver=table.TableResolver(ksql_client=ksql_client),
        transitioner=table.TableTransitioner(ksql_client=ksql_client)))

    return components
