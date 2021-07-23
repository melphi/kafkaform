import dataclasses
from typing import List, Optional

from app import model
from app.component.stream import resolver


class TableResolver(resolver.BaseStreamResolver):
    def system_get(self, name: str) -> Optional[model.SpecItem]:
        info = self._ksql_client.resource_describe(name)
        if info:
            params = model.StreamParams(sql=info.sql)
            return model.SpecItem(
                name=info.name,
                resource_type=model.RESOURCE_TABLE,
                params=dataclasses.asdict(params),
                schema_name=None)
        return None

    def system_list(self) -> List[str]:
        return self._ksql_client.table_list()
