from typing import Dict, List, Optional

import requests

from app.client import sqlbuilder
from app import model


class KsqlException(Exception):
    def __init__(self, statement: str, msg: str):
        self.statement = statement
        self.msg = msg

    def __str__(self):
        return f"KSQL failed to execute statement [{self.statement}], error: {self.msg}"


class KsqlClient:
    """Mockable Kafka KSQL client"""

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


class KsqlClientImpl(KsqlClient):
    """Rest API Kafka KSQL client"""

    _NOT_FOUND_PREFIX = "Could not find"
    _STATE_SUCCESS = "SUCCESS"

    def __init__(self, *, ksql_url: str):
        self._ksql_url = ksql_url
        self._sql_builder = sqlbuilder.Builder()

    def execute_command(self, sql: str) -> None:
        data = self._execute_sql_request(sql, {})
        result = self._get_only_record(data)
        assert result.get("commandStatus") and result["commandStatus"].get("status") == self._STATE_SUCCESS, \
            f"Unexpected KSQL command response [{str(result)}]"

    def resource_describe(self, name: str) -> Optional[model.ResourceInfo]:
        try:
            data = self._execute_sql_request("DESCRIBE {{ name }};", {"name": name})
            item = self._get_only_record(data)
            return model.ResourceInfo(
                name=item["sourceDescription"]["name"],
                sql=item["sourceDescription"]["statement"])
        except KsqlException as e:
            if self._NOT_FOUND_PREFIX in e.msg:
                return None
            raise e

    def stream_list(self) -> List[str]:
        data = self._execute_sql_request("SHOW STREAMS;", {})
        item = self._get_only_record(data)
        return [stream["name"] for stream in item.get("streams")]

    def stream_drop(self, name: str) -> None:
        raise NotImplementedError()

    def table_list(self) -> List[str]:
        data = self._execute_sql_request("SHOW TABLES;", {})
        item = self._get_only_record(data)
        return [stream["name"] for stream in item.get("tables")]

    def table_drop(self, name: str) -> None:
        raise NotImplementedError()

    def udf_list(self) -> List[str]:
        raise NotImplementedError()

    def udf_describe(self, name: str) -> Optional[model.UdfInfo]:
        raise NotImplementedError()

    def _assert_resource_type(self, sql: str, resource_type: str) -> None:
        parts = sql.strip().upper().split(" ")
        if ["CREATE", resource_type.upper()] in parts[:2] \
                or ["CREATE", "OR", "REPLACE", resource_type.upper()] in parts[:4]:
            return
        raise ValueError(f"Resource type is not a {resource_type.upper()} in command [{sql}]")

    def _execute_sql_request(self, sql: str, params: dict) -> List[Dict[str, any]]:
        ksql = self._sql_builder.safe_interpolate(sql, params)
        resp = requests.post(f"{self._ksql_url}/ksql", json={"ksql": ksql})
        return self._parse_response(resp, ksql)

    def _parse_response(self, resp: requests.Response, ksql: str) -> List[Dict[str, any]]:
        data = resp.json()
        if resp.status_code != 200:
            if data.get("message"):
                error_msg = data['message']
            else:
                error_msg = str(data)
            if data.get("statementText"):
                error_sql = data["statementText"]
            else:
                error_sql = ksql
            raise KsqlException(error_sql, error_msg)
        return data

    def _get_only_record(self, records: List[Dict[str, any]]) -> dict:
        assert len(records) == 1, f"Expected 1 record as sql response, [{len(records)}] found."
        return records[0]
