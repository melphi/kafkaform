import dataclasses
from typing import Optional, List

from app import model
from app.component import component


class BaseConnectResolver(component.Resolver):
    def __init__(self, connect_client: client.ConnectClient, connector_type: str):
        self._connect_client = connect_client
        self._connector_type = connector_type

    def describe(self, target: model.SpecItem) -> model.Description:
        class_name = target.params.get("connector.class")
        if not class_name:
            raise ValueError(f"Missing required parameter [connector.class]")
        depends = [model.Dependency(
            name=class_name,
            resource_type=model.RESOURCE_CONNECTOR_CLASS)]
        return model.Description(
            depends=depends,
            schema=self._get_schema(target),
            spec=target)

    def system_list(self) -> List[str]:
        connectors = self._connect_client.connectors_list()
        for connector in connectors:
            info = self._connect_client.connector_get(connector)
            # It assumes that the connector class name contains the connector type.
            if self._connector_type in info.config["connector.class"].lower():
                yield connector

    def system_get(self, name: str) -> Optional[model.SpecItem]:
        info = self._connect_client.connector_get(name)
        if info:
            params = model.ConnectParams(config=info.config)
            return model.SpecItem(
                name=info.name,
                resource_type=self._connector_type,
                params=dataclasses.asdict(params),
                schema_name=None)
        return None

    def _get_schema(self, target: model.SpecItem) -> Optional[model.SchemaParams]:
        raise NotImplementedError()


# TODO: Return list of connector classes.
class ConnectorClassResolver(component.Resolver):
    def describe(self, target: model.SpecItem) -> model.Description:
        raise NotImplementedError()

    def system_list(self) -> List[str]:
        raise NotImplementedError()

    def system_get(self, name: str) -> Optional[model.SpecItem]:
        raise NotImplementedError()
