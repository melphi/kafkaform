import os

from dataclasses import dataclass


@dataclass
class Config:
    kafka_bootstrap_server: str
    kafka_connect_url: str
    kafka_ksql_url: str


def from_environment() -> Config:
    try:
        return Config(
            kafka_bootstrap_server=os.environ["KAFKA_BOOTSTRAP_SERVER"],
            kafka_connect_url=os.environ["KAFKA_CONNECT_URL"],
            kafka_ksql_url=os.environ["KAFKA_KSQL_URL"])
    except KeyError as e:
        raise ValueError(f"Required environment variable not set [{str(e)}]")
