from typing import List

import re

from app import model
from app.actioner.validate import validate


class NamingConsistencyValidator(validate.Validator):
    """Makes sure item name matches the resource name (topic, table, etc) which will be created"""

    def validate_target(
            self, target: model.Spec, descriptions: List[model.Description]) -> bool:
        # if source.target.config.get("topic"):
        #     self._check_pattern(source.target.config["topic"], "source.config.topic")
        # TODO: Source name equals topic name
        # TODO: Stream name equals resource name / topic name (?)
        raise NotImplementedError()


class NameConventionValidator(validate.Validator):
    """Validates naming convention"""

    _PATTERN = re.compile(r"\S+__\S+__\S+__v\d+")

    def validate_target(
            self, target: model.Spec, descriptions: List[model.Description]) -> bool:
        for spec in target.specs:
            self._check_pattern(spec)
        return True

    def _check_pattern(self, spec: model.SpecItem) -> None:
        if not spec.name:
            raise ValueError(f"Name is a required field for resource [{spec.resource_type}].")
        if not self._PATTERN.match(spec.name):
            raise ValueError(f"Invalid name [{spec.name}] for resource type [{spec.resource_type}]. "
                             f"Example of valid pattern [layer__resourcetype__project__entityname__v1]")


class NameUniquenessValidator(validate.Validator):
    """Validates name uniqueness among items"""

    def validate_target(
            self, target: model.Spec, descriptions: List[model.Description]) -> bool:
        names = {}
        for spec in target.specs:
            if spec.name in names:
                raise ValueError(f"Names must be unique, duplicate found [{spec.name}]")
            names[spec.name] = True
        return True
