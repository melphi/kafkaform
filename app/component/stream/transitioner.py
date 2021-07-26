import logging

from app import model, client
from app.component import component


class BaseStreamTransitioner(component.Transitioner):
    _LOG = logging.getLogger(__name__)

    def __init__(self, ksql_client: client.KsqlClient, resource_type: str):
        self._ksql_client = ksql_client
        self._resource_type = resource_type

    def apply(self, delta: model.DeltaItem) -> None:
        if delta.deleted:
            try:
                self._ksql_client.stream_drop(delta.current.name)
            except Exception as e:
                raise ValueError(f"Error while deleting stream [{delta.current.name}]: {str(e)}")
            self._LOG.info(f"{self._resource_type.capitalize()} [{delta.current.name}] deleted")
        else:
            assert delta.target, "Missing stream target object"
            try:
                if self._resource_type == model.RESOURCE_STREAM:
                    sql = model.StreamParams(**delta.target.params).sql
                elif self._resource_type == model.RESOURCE_TABLE:
                    sql = model.TableParams(**delta.target.params).sql
                else:
                    raise ValueError(f"Unsupported resource type {self._resource_type}")
                self._ksql_client.execute_command(sql)
            except Exception as e:
                raise ValueError(f"Error while updating stream [{delta.target.name}]: {str(e)}")
            if delta.current:
                self._LOG.info(f"{self._resource_type.capitalize()} [{delta.target.name}] updated")
            else:
                self._LOG.info(f"{self._resource_type.capitalize()} [{delta.target.name}] created")


class StreamTransitioner(BaseStreamTransitioner):
    def __init__(self, ksql_client: client.KsqlClient):
        super().__init__(ksql_client, model.RESOURCE_STREAM)
