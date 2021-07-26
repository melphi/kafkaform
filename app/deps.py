from typing import List

from app import actioner, client, conf
from app.component import registered, component


class Dependencies:
    """Initialises application dependencies based on configuration"""

    def __init__(self, cfg: conf.Config):
        self.connect_client = client.ConnectClientImpl(connect_url=cfg.kafka_connect_url)
        self.ksql_client = client.KsqlClientImpl(ksql_url=cfg.kafka_ksql_url)

        components = self._create_components()

        parsers = [comp.parser for comp in components if comp.parser]
        self.parser = actioner.Parser(parsers=parsers)

        resolvers_map = {comp.resource_type: comp.resolver for comp in components if comp.resolver}
        self.resolver = actioner.Resolver(resolvers_map=resolvers_map)

        transitioners_map = {comp.resource_type: comp.transitioner for comp in components if comp.transitioner}
        self.transitioner = actioner.Transitioner(transitioners_map=transitioners_map)

    def _create_components(self) -> List[component.Component]:
        components = registered.build_all(
            connect_client=self.connect_client,
            ksql_client=self.ksql_client)

        names = [comp.resource_type for comp in components]
        assert len(components) == len(set(names)), \
            f"Resource type in components must be unique, duplicated found [{names}]"

        return components
