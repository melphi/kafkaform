import logging
import time

from app import model, client
from app.component import component


class BaseStreamTransitioner(component.Transitioner):
    _LOG = logging.getLogger(__name__)

    def __init__(self, ksql_client: client.KsqlClient, resource_type: str):
        self._ksql_client = ksql_client
        self._resource_type = resource_type

    def drop(self, spec: model.SpecItem, *, cascade: bool = False) -> None:
        info = self._ksql_client.resource_describe(spec.name)
        if info:
            for dependency in info.dependencies:
                if dependency.resource_type == model.RESOURCE_QUERY:
                    self._ksql_client.query_terminate(dependency.name)
                else:
                    raise ValueError(f"Drop operation does not support dependency type [{dependency.resource_type}]")
            try:
                if info.resource_type == model.RESOURCE_STREAM:
                    self._ksql_client.stream_drop(info.name)
                elif info.resource_type == model.RESOURCE_TABLE:
                    self._ksql_client.table_drop(info.name)
                else:
                    raise ValueError(f"Drop operation does not support resource type [{spec.resource_type}]")
            except Exception as e:
                raise e

    def apply(self, delta: model.DeltaItem) -> None:
        if delta.deleted:
            try:
                self._drop_resource(delta.current)
            except Exception as e:
                raise ValueError(f"Error while deleting stream [{delta.current.name}]: {str(e)}")
            self._LOG.info(f"{self._resource_type.capitalize()} [{delta.current.name}] deleted")
        else:
            assert delta.target, "Missing stream target object"
            try:
                sql = self._get_sql(delta)
                if delta.current:
                    self._drop_resource(delta.current)
                self._ksql_client.execute_command(sql)
            except Exception as e:
                raise ValueError(f"Error while updating stream [{delta.target.name}]: {str(e)}")
            if delta.current:
                self._LOG.info(f"{self._resource_type.capitalize()} [{delta.target.name}] replaced")
            else:
                self._LOG.info(f"{self._resource_type.capitalize()} [{delta.target.name}] created")

    def validate(self, delta: model.DeltaItem) -> None:
        if delta.target:
            sql = self._get_sql(delta)
            try:
                self._ksql_client.syntax_check(sql)
            except client.KsqlException as e:
                raise ValueError(f"Invalid syntax: {str(e)}")

    def _drop_resource(self, spec: model.SpecItem) -> None:
        if spec.resource_type == model.RESOURCE_STREAM:
            self._ksql_client.stream_drop(spec.name)
        elif spec.resource_type == model.RESOURCE_TABLE:
            self._ksql_client.table_drop(spec.name)
        else:
            raise ValueError(f"Unsupported resource type [{self._resource_type}]")
        self._wait_for_dropped(spec.name)

    def _get_sql(self, delta: model.DeltaItem) -> str:
        if self._resource_type == model.RESOURCE_STREAM:
            return model.StreamParams(**delta.target.params).sql
        elif self._resource_type == model.RESOURCE_TABLE:
            return model.TableParams(**delta.target.params).sql
        raise ValueError(f"Unsupported resource type [{self._resource_type}]")

    def _wait_for_dropped(self, resource_name: str) -> None:
        for i in range(5):
            if not self._ksql_client.resource_describe(resource_name):
                return
            time.sleep(0.2 * i)
        raise ValueError(f"Resource [{resource_name}] not deleted within the timeout")


class StreamTransitioner(BaseStreamTransitioner):
    def __init__(self, ksql_client: client.KsqlClient):
        super().__init__(ksql_client, model.RESOURCE_STREAM)
