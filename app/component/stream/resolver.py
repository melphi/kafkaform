import dataclasses
from typing import Dict, List, Optional

from app.component import component
from app import model, client


class BaseStreamResolver(component.Resolver):
    def __init__(self, *, ksql_client: client.KsqlClient):
        self._ksql_client = ksql_client
        self._sys_udf: Dict[str, model.UdfInfo] = {}

    def equals(self, current: model.SpecItem, target: model.SpecItem) -> bool:
        if current.resource_type != target.resource_type \
                or current.name.lower() != target.name.lower():
            return False
        for key, val in target.params.items():
            if key == 'sql':
                current_sql = current.params['sql'].strip().upper()
                if current_sql.endswith(";"):
                    current_sql = current_sql[:-1]
                target_sql = val.strip().upper()
                if target_sql.endswith(";"):
                    target_sql = target_sql[:-1]
                if current_sql != target_sql:
                    return False
            else:
                if key not in current.params or current.params[key] != val:
                    return False
        return True

    def describe(self, target: model.SpecItem) -> model.Description:
        params = model.StreamParams(**target.params)
        depends = self._get_dependencies(params.sql)
        schema = self._get_schema(params.sql)
        return model.Description(
            depends=depends,
            schema=schema,
            spec=target)

    def system_list(self) -> List[str]:
        raise NotImplementedError()

    def system_get(self, name: str) -> Optional[model.SpecItem]:
        raise NotImplementedError()

    def _get_dependencies(self, sql: str) -> List[model.Dependency]:
        # TODO: Return udf and table_or_stream dependencies
        return list()

    def _get_udf(self, name: str) -> Optional[model.UdfInfo]:
        if name in self._sys_udf:
            return self._sys_udf[name]
        udf = self._ksql_client.udf_describe(name)
        if udf:
            self._sys_udf[name] = udf
        return udf

    def _get_schema(self, sql: str) -> model.SchemaParams:
        # TODO: Implement schema recognition, load UDF info. Note: UDF schema is variable.
        return None


class StreamResolver(BaseStreamResolver):
    def system_get(self, name: str) -> Optional[model.SpecItem]:
        info = self._ksql_client.resource_describe(name)
        if info:
            params = model.StreamParams(sql=info.sql)
            return model.SpecItem(
                name=info.name,
                resource_type=model.RESOURCE_STREAM,
                params=dataclasses.asdict(params),
                schema_name=None)
        return None

    def system_list(self) -> List[str]:
        return self._ksql_client.stream_list()
