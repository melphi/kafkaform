import dataclasses
from typing import Optional, List

from app import model, client
from app.component import component


class BaseConnectResolver(component.Resolver):
    _KNOWN_SINKS = []
    _KNOWN_SOURCES = ["io.confluent.kafka.connect.datagen.DatagenConnector"]

    def __init__(self, *, connect_client: client.ConnectClient, connector_type: str):
        self._connect_client = connect_client
        self._connector_type = connector_type

    def describe(self, target: model.SpecItem) -> model.Description:
        params = model.ConnectParams(**target.params)
        class_name = params.config.get("connector.class")
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
        connectors = list()
        names = self._connect_client.connectors_list()
        for name in names:
            info = self._connect_client.connector_get(name)
            if self._is_type(info, self._connector_type):
                connectors.append(name)
        return connectors

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

    def equals(self, current: model.SpecItem, target: model.SpecItem) -> bool:
        target_params = model.ConnectParams(**target.params)
        current_params = model.ConnectParams(**current.params)
        for key, value in target_params.config.items():
            if key not in current_params.config or current_params.config[key] != str(value):
                return False
        return current.name.lower() == target.name.lower() \
            and current.resource_type == target.resource_type

    def _is_type(self, info: model.ConnectorInfo, connector_type: str) -> bool:
        connector_class = info.config["connector.class"]
        if model.RESOURCE_SOURCE in connector_class.lower() \
                or connector_class in self._KNOWN_SOURCES:
            return connector_type == model.RESOURCE_SOURCE
        elif model.RESOURCE_SINK in connector_class.lower() \
                or connector_class in self._KNOWN_SINKS:
            return connector_type == model.RESOURCE_SINK
        raise ValueError(f"Can not recognise type of connector class [{connector_class}]. "
                         f"As class name does not contain valuable information, "
                         f"update list of known sinks and sources.")

    def _get_schema(self, target: model.SpecItem) -> Optional[model.SchemaParams]:
        raise NotImplementedError()


class ConnectorClassResolver(component.Resolver):
    def __init__(self, *, connect_client: client.ConnectClient):
        self._connect_client = connect_client

    def describe(self, target: model.SpecItem) -> model.Description:
        return model.Description(
            depends=list(),
            spec=target,
            schema=None)

    def system_list(self) -> List[str]:
        return self._connect_client.plugins_list()

    def system_get(self, name: str) -> Optional[model.SpecItem]:
        # TODO: Consider to cache plugin list call.
        if name in self._connect_client.plugins_list():
            return model.SpecItem(name=name,
                                  resource_type=model.RESOURCE_CONNECTOR_CLASS,
                                  params={},
                                  schema_name=None)
        return None

    def equals(self, current: model.SpecItem, target: model.SpecItem) -> bool:
        return current.resource_type == target.resource_type \
               and current.name.lower() == target.name.lower() \
               and current.params == target.params
