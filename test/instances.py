from typing import Dict, List

from app import component
from test import mock

MOCK_ADMIN_CLIENT = mock.MockAdminClient()
MOCK_CONNECT_CLIENT = mock.MockConnectClient()
MOCK_KSQL_CLIENT = mock.MockKsqlClient()


def _load_components() -> List[component.Component]:
    return component.build_all(
        admin_client=MOCK_ADMIN_CLIENT,
        connect_client=MOCK_CONNECT_CLIENT,
        ksql_client=MOCK_KSQL_CLIENT)


def _load_parsers_map() -> Dict[str, component.Parser]:
    parsers = {}
    components = _load_components()
    for comp in components:
        if comp.parser:
            parsers[comp.resource_type] = comp.parser
    return parsers


PARSERS_MAP = _load_parsers_map()
