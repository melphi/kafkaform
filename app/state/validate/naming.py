import re

from app import spec
from app.state import delta, validate, resource


class NamingConventionValidator(validate.Validator):
    """Validates naming convention"""

    _PATTERN = re.compile(r"\S+__\S+__\S+__v\d+")

    def validate(self, *,
                 target: spec.Spec,
                 changes: delta.DeltaState,
                 res: resource.Resources) -> bool:
        for sink in changes.delta_sinks:
            self._check_pattern(sink.target.name, "sink.name")
        for source in changes.delta_sources:
            self._check_pattern(source.target.name, "source.name")
        for stream in changes.delta_streams:
            self._check_pattern(stream.target.name, "stream.name")
        return True

    def _check_pattern(self, value: str, field_name: str) -> None:
        if not value:
            raise ValueError(f"Invalid field [{field_name}] value, it can not be empty.")
        if not self._PATTERN.match(value):
            raise ValueError(f"Invalid field [{field_name}] value [{value}]. "
                             f"Example of valid pattern [layer__resourcetype__project__entityname__v1]")


class NamingConsistencyValidator(validate.Validator):
    """Makes sure item name matches the resource name (topic, table, etc) which will be created"""

    def validate(self, *, target: spec.Spec, changes: delta.DeltaState) -> bool:
        # if source.target.config.get("topic"):
        #     self._check_pattern(source.target.config["topic"], "source.config.topic")
        # TODO: Source name equals topic name
        # TODO: Stream name equals resource name / topic name (?)
        raise NotImplementedError()


class UniqueNamesValidator(validate.Validator):
    """Validates name uniqueness among items"""

    def validate(self, *, target: spec.Spec, changes: delta.DeltaState) -> bool:
        # if source.target.config.get("topic"):
        #     self._check_pattern(source.target.config["topic"], "source.config.topic")
        # TODO: Source name equals topic name
        # TODO: Stream name equals resource name / topic name (?)
        raise NotImplementedError()
