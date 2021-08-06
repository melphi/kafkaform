import logging

from app import actioner, model


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


class KafkaDescribeCommand(Command):
    NAME = "kafka:describe"
    HELP = "Prints detailed resources information about the system"

    def run(self) -> None:
        raise NotImplementedError()


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


class KafkaPlanCommand(Command):
    NAME = "kafka:plan"
    HELP = "Shows the changes required"

    _LOG = logging.getLogger(__name__)

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
