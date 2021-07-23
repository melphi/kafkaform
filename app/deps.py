from app import conf, client


class Dependencies:
    """Initialises application dependencies based on configuration"""

    def __init__(self, cfg: conf.Config):
        self.connect_client = client.ConnectClientImpl(connect_url=cfg.kafka_connect_url)
        self.ksql_client = client.KsqlClientImpl(ksql_url=cfg.kafka_ksql_url)
