from typing import List, Optional

from app import model

import requests


class ConnectClient:
    """Mockable Kafka Connect client"""

    def connector_delete(self, name: str) -> None:
        raise NotImplementedError()

    def connector_get(self, name: str) -> Optional[model.ConnectorInfo]:
        raise NotImplementedError()

    def connectors_list(self) -> List[str]:
        raise NotImplementedError()

    def connector_update(self, name: str, config: dict) -> model.ConnectorInfo:
        raise NotImplementedError()

    def plugins_list(self) -> List[str]:
        raise NotImplementedError()


class ConnectClientImpl(ConnectClient):
    """Rest API Kafka Connect client"""

    def __init__(self, *, connect_url: str) -> None:
        assert connect_url, "Missing connect url"
        self._connect_url = connect_url
        if self._connect_url.endswith("/"):
            self._connect_url = self._connect_url[:-1]

    def connector_delete(self, name: str) -> None:
        assert name, "Name can not be empty"
        resp = requests.delete(f"{self._connect_url}/connectors/{name}")
        assert resp.status_code in [204, 400], \
            f"Invalid status code [{resp.status_code}]."

    def connector_get(self, name: str) -> Optional[model.ConnectorInfo]:
        assert name, "Connector name can not be empty"
        resp = requests.get(f"{self._connect_url}/connectors/{name}")
        if resp.status_code == 200:
            data = resp.json()
            return self._create_info(
                name=data["name"],
                config=data["config"],
                tasks=data["tasks"])
        elif resp.status_code == 404:
            return None
        else:
            raise ValueError(f"Invalid status code [{resp.status_code}]: {resp.text}.")

    def connectors_list(self) -> List[str]:
        resp = requests.get(f"{self._connect_url}/connectors")
        assert resp.status_code == 200, f"Invalid status code [{resp.status_code}]: {resp.text}."
        return resp.json()

    def connector_update(self, name: str, config: dict) -> model.ConnectorInfo:
        resp = requests.put(f"{self._connect_url}/connectors/{name}/config", json=config)
        if resp.status_code in [200, 201]:
            data = resp.json()
            return self._create_info(
                name=data["name"],
                config=data["config"],
                tasks=data["tasks"])
        elif resp.status_code == 409:
            raise ValueError("Cluster is re-balancing, try later")
        raise ValueError(f"Invalid Kafka Connect response [{resp.status_code}]: {resp.text}.")

    def plugins_list(self) -> List[str]:
        resp = requests.get(f"{self._connect_url}/connector-plugins")
        assert resp.status_code == 200, f"Invalid status code [{resp.status_code}]: {resp.text}."
        return [item["class"] for item in resp.json()]

    def _create_info(self, *, name: str, config: dict, tasks: list) -> model.ConnectorInfo:
        return model.ConnectorInfo(name=name, config=config, tasks=tasks)
