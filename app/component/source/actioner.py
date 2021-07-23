from app import client
from app.component.sink import actioner


class SourceActioner(actioner.BaseConnectActioner):
    def __init__(self, connect_client: client.ConnectClient):
        super().__init__(connect_client, "source")
