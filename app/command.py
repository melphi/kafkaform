import logging
import json

from app import actioner, model, client


class Command:
    """Base class for commands"""

    def run(self) -> any:
        raise NotImplementedError()


class ConfigDebugCommand(Command):
    NAME = "config:debug"
    HELP = "Debug utilities"

    def __init__(self, *, file_path: str, parser: actioner.Parser):
        self._file_path = file_path
        self._parser = parser

    def run(self) -> str:
        rendered = self._parser.render(self._file_path)
        print(f"Rendered configuration file {self._file_path}:\n\n")
        print(rendered)
        return rendered


class KafkaApplyCommand(Command):
    NAME = "kafka:apply"
    HELP = "Applies the configuration to the system"

    _LOG = logging.getLogger(__name__)

    def __init__(self, *,
                 parser: actioner.Parser,
                 resolver: actioner.Resolver,
                 transitioner: actioner.Transitioner,
                 file_path: str,
                 ask_confirmation: bool = True):
        self._parser = parser
        self._resolver = resolver
        self._transitioner = transitioner
        self._file_path = file_path
        self._ask_confirmation = ask_confirmation

    def run(self) -> model.Delta:
        target = self._parser.parse(self._file_path)
        if target == model.EMPTY_SPEC:
            raise ValueError("Parsed files do not contain any resource")
        delta = self._resolver.load_checked_delta(target)
        if delta == model.EMPTY_DELTA:
            self._LOG.info("System is up to date")
        else:
            self._transitioner.transit_state(delta, self._ask_confirmation)
        return delta


class KafkaDumpCommand(Command):
    NAME = "kafka:dump"
    HELP = "Dumps the current state of the system to file"

    def __init__(self, *,
                 parser: actioner.Parser,
                 resolver: actioner.Resolver,
                 dest_path: str):
        self._resolver = resolver
        self._parser = parser
        self._dest_path = dest_path

    def run(self) -> None:
        with open(self._dest_path, "w") as target:
            data = self._resolver.load_current()
            self._parser.save(data=data, target=target)


class KafkaEraseCommand(Command):
    NAME = "kafka:erase"
    HELP = "Removes all resources listed in the configuration file from Kafka"

    def __init__(self, *,
                 parser: actioner.Parser,
                 transitioner: actioner.Transitioner,
                 file_path: str,
                 ask_confirmation: bool = True):
        self._parser = parser
        self._transitioner = transitioner
        self._file_path = file_path
        self._ask_confirmation = ask_confirmation

    def run(self) -> any:
        target = self._parser.parse(self._file_path)
        if target == model.EMPTY_SPEC:
            raise ValueError("Parsed files do not contain any resource")
        self._transitioner.erase(target, self._ask_confirmation)
        return target


class KafkaPlanCommand(Command):
    NAME = "kafka:plan"
    HELP = "Shows the changes required"

    def __init__(self, *,
                 parser: actioner.Parser,
                 resolver: actioner.Resolver,
                 file_path: str):
        self._file_path = file_path
        self._parser = parser
        self._resolver = resolver

    def run(self) -> model.Delta:
        target = self._parser.parse(self._file_path)
        return self._resolver.load_checked_delta(target)


class KafkaSqlCommand(Command):
    NAME = "kafka:sql"
    HELP = "Runs SQL queries and prints the result"

    _LOG = logging.getLogger(__name__)

    def __init__(self, *,
                 ksql_client: client.KsqlClient,
                 sql: str):
        self._ksql_client = ksql_client
        self._sql = sql

    def run(self) -> None:
        res = self._ksql_client.execute_query(self._sql)
        self._LOG.info(f"\nResults:\n\n")
        for record in res:
            self._LOG.info(f"{json.dumps(record, indent=2)}\n")
