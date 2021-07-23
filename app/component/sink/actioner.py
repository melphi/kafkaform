import logging

from app import model, client
from app.component import component


class BaseConnectActioner(component.Actioner):
    _LOG = logging.getLogger(__name__)

    def __init__(self, connect_client: client.ConnectClient, connector_type: str):
        self._connect_client = connect_client
        self._connector_type = connector_type

    def apply(self, delta: model.DeltaItem) -> None:
        if delta.deleted:
            try:
                self._connect_client.connector_delete(delta.current.name)
            except Exception as e:
                raise ValueError(f"Error while deleting {self._connector_type} "
                                 f"connector [{delta.current.name}]: {str(e)}")
            self._LOG.info(f"Source connector [{delta.current.name}] deleted")
        else:
            assert delta.target, "Missing connector target object"
            try:
                params = model.ConnectParams(**delta.target.params)
                self._connect_client.connector_update(delta.target.name, params.config)
            except Exception as e:
                raise ValueError(f"Error while updating {self._connector_type} "
                                 f"connector [{delta.target.name}]: {str(e)}")
            if delta.current:
                self._LOG.info(f"{self._connector_type.capitalize()} connector [{delta.target.name}] updated")
            else:
                self._LOG.info(f"{self._connector_type.capitalize()} connector [{delta.target.name}] created")


class SinkActioner(BaseConnectActioner):
    def __init__(self, connect_client: client.ConnectClient):
        super().__init__(connect_client, "sink")

