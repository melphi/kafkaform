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

    def _get_sql(self, delta: model.DeltaItem) -> str:
        if self._resource_type == model.RESOURCE_STREAM:
            return model.StreamParams(**delta.target.params).sql
        elif self._resource_type == model.RESOURCE_TABLE:
            return model.TableParams(**delta.target.params).sql
        raise ValueError(f"Unsupported resource type [{self._resource_type}]")


class StreamTransitioner(BaseStreamTransitioner):
    def __init__(self, ksql_client: client.KsqlClient):
        super().__init__(ksql_client, model.RESOURCE_STREAM)
