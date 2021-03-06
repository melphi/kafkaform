from app import model, client
from app.component.stream import transitioner


class TableTransitioner(transitioner.BaseStreamTransitioner):
    def __init__(self, ksql_client: client.KsqlClient):
        super().__init__(ksql_client, model.RESOURCE_STREAM)
