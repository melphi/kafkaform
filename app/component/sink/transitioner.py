from app import client
from app.component.connect import transitioner


class SinkTransitioner(transitioner.BaseConnectTransitioner):
    def __init__(self, *, connect_client: client.ConnectClient):
        super().__init__(connect_client=connect_client, connector_type="sink")
