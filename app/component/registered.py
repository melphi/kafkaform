from typing import List

from app import client, model
from app.component import component, connect, schema, sink, source, stream, table, topic


def build_all(*,
              admin_client: client.AdminClient,
              connect_client: client.ConnectClient,
              ksql_client: client.KsqlClient) -> List[component.Component]:
    components = list()

    # Connector class
    components.append(component.Component(
        resource_type=model.RESOURCE_CONNECTOR_CLASS,
        parser=None,
        resolver=connect.ConnectorClassResolver(connect_client=connect_client),
        transitioner=None))

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

    # Topic
    components.append(component.Component(
        resource_type=model.RESOURCE_TOPIC,
        parser=topic.TopicParser(),
        resolver=topic.TopicResolver(admin_client=admin_client),
        transitioner=topic.TopicTransitioner(admin_client=admin_client)))

    return components
