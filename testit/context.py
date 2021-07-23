import os
from testcontainers import compose

from app import conf


class ITestContext:
    _COMPOSE_PATH = "resources/"
    _COMPOSE_FILE = "docker-compose.it.yml"

    def __enter__(self):
        self._compose = compose.DockerCompose(
                self._COMPOSE_PATH,
                compose_file_name=self._COMPOSE_FILE)
        self._compose.start()
        self._compose.wait_for(self._get_kafka_connect_url())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._compose.stop()
        cleanup_cmd = f"docker-compose -f {self._COMPOSE_PATH}{self._COMPOSE_FILE} down -v --remove-orphans"
        assert os.system(cleanup_cmd) == 0, f"Error while executing cleanup code [{cleanup_cmd}]"

    def get_config(self) -> conf.Config:
        return conf.Config(
            kafka_broker_address=self._get_kafka_broker_address(),
            kafka_connect_url=self._get_kafka_connect_url(),
            kafka_ksql_url=self._get_kafka_ksql_url())

    def _get_kafka_broker_address(self) -> str:
        return f"127.0.0.1:{self._compose.get_service_port('broker', 9092)}"

    def _get_kafka_connect_url(self) -> str:
        return f"http://127.0.0.1:{self._compose.get_service_port('connect', 8083)}"

    def _get_kafka_ksql_url(self) -> str:
        return f"http://127.0.0.1:{self._compose.get_service_port('ksqldb-server', 8088)}"
