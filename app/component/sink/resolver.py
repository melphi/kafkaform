from typing import Optional

from app import model, client
from app.component.connect import resolver


class SinkResolver(resolver.BaseConnectResolver):
    def __init__(self, *, connect_client: client.ConnectClient):
        super().__init__(connect_client, model.RESOURCE_SINK)

    def _get_schema(self, target: model.SpecItem) -> Optional[model.SchemaParams]:
        return None
