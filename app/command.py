import logging

from app import actioner, client, spec, state


class Command:
    """Base class for commands"""

    def run(self) -> any:
        raise NotImplementedError()


class ConfigDebugCommand(Command):
    NAME = "config:debug"
    HELP = "Debug utilities"

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._parser = spec.Parser()

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
                 connect_client: client.ConnectClient,
                 ksql_client: client.KsqlClient,
                 file_path: str,
                 ask_confirmation: bool = True):
        self._actioner = actioner.Actioner(
            connect_client=connect_client,
            ksql_client=ksql_client)
        self._loader = state.StateLoader(
            connect_client=connect_client,
            ksql_client=ksql_client)
        self._file_path = file_path
        self._ask_confirmation = ask_confirmation

    def run(self) -> state.DeltaState:
        target = spec.PARSER.parse(self._file_path)
        if target == spec.EMPTY_SPEC:
            raise ValueError("Parsed files do not contain any resource")
        delta = self._loader.load_system_delta(target)
        if delta == state.EMPTY_DELTA:
            self._LOG.info("System is up to date")
        else:
            self._actioner.transit_state(delta, self._ask_confirmation)
        return delta


class KafkaDescribeCommand(Command):
    NAME = "kafka:describe"
    HELP = "Prints detailed resources information about the system"

    def run(self) -> None:
        raise NotImplementedError()


class KafkaDumpCommand(Command):
    NAME = "kafka:dump"
    HELP = "Dumps the current state of the system to file"

    def __init__(self, *,
                 connect_client: client.ConnectClient,
                 ksql_client: client.KsqlClient,
                 dest_path: str):
        self._loader = state.StateLoader(
            connect_client=connect_client,
            ksql_client=ksql_client)
        self._dest_path = dest_path

    def run(self) -> None:
        with open(self._dest_path, "w") as target:
            data = self._loader.load_system_state()
            spec.PARSER.save(data=data, target=target)


class KafkaPlanCommand(Command):
    NAME = "kafka:plan"
    HELP = "Shows the changes required"

    _LOG = logging.getLogger(__name__)

    def __init__(self, *,
                 connect_client: client.ConnectClient,
                 ksql_client: client.KsqlClient,
                 file_path: str):
        self._file_path = file_path
        self._loader = state.StateLoader(
            connect_client=connect_client,
            ksql_client=ksql_client)

    def run(self) -> state.DeltaState:
        target = spec.PARSER.parse(self._file_path)
        return self._loader.load_system_delta(target)
