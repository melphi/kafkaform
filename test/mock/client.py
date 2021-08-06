from typing import List, Optional

from app import client, model


class MockAdminClient(client.AdminClient):
    def topic_create(
            self, *, topic_name: str, num_partitions: int, replication_factor: int
    ) -> None:
        raise NotImplementedError()

    def topic_describe(self, topic_name: str) -> Optional[model.TopicInfo]:
        raise NotImplementedError()

    def topic_drop(self, topic_name: str) -> None:
        raise NotImplementedError()

    def topics_list(self) -> List[str]:
        raise NotImplementedError()


class MockConnectClient(client.ConnectClient):
    def connector_delete(self, name: str) -> None:
        raise NotImplementedError()

    def connector_get(self, name: str) -> Optional[model.ConnectorInfo]:
        raise NotImplementedError()

    def connectors_list(self) -> List[str]:
        raise NotImplementedError()

    def connector_update(self, name: str, config: dict) -> model.ConnectorInfo:
        raise NotImplementedError()

    def connector_validate(self, name: str, config: dict) -> None:
        raise NotImplementedError()

    def plugins_list(self) -> List[str]:
        raise NotImplementedError()


class MockKsqlClient(client.KsqlClient):
    def execute_command(self, sql: str) -> None:
        raise NotImplementedError()

    def resource_describe(self, name: str) -> Optional[model.ResourceInfo]:
        raise NotImplementedError()

    def stream_list(self) -> List[str]:
        raise NotImplementedError()

    def stream_drop(self, name: str) -> None:
        raise NotImplementedError()

    def table_list(self) -> List[str]:
        raise NotImplementedError()

    def table_drop(self, name: str) -> None:
        raise NotImplementedError()

    def udf_list(self) -> List[str]:
        raise NotImplementedError()

    def udf_describe(self, name: str) -> Optional[model.UdfInfo]:
        raise NotImplementedError()
