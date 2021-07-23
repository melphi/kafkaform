from typing import Optional

from app import model, client
from app.component.sink import resolver


class SourceResolver(resolver.BaseConnectResolver):
    def __init__(self, connect_client: client.ConnectClient):
        super().__init__(connect_client, model.RESOURCE_SOURCE)

    def _get_schema(self, target: model.SpecItem) -> Optional[model.SchemaParams]:
        return None
