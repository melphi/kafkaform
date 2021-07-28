from typing import Dict

import logging

from app import model
from app.component import component


class Transitioner:
    _CREATE = "create"
    _DELETE = "delete"
    _UPDATE_OR_REPLACE = "update or replace"

    """Performs system state transit actions"""

    _LOG = logging.getLogger(__name__)

    def __init__(self, *, transitioners_map: Dict[str, component.Transitioner]):
        self._transitioners_map = transitioners_map

    def transit_state(self, changes: model.Delta, ask_confirmation: bool) -> None:
        self._validate_changes(changes)
        if ask_confirmation:
            self._LOG.info("Planned changes..")
            self._LOG.info(self._pretty_print(changes))
            choice = input("Confirm changes? [Y/n]\n")
            print()
            if choice != "Y":
                self._LOG.warning("Operation aborted")
                exit(1)
        self._transit_states(changes)

    def _validate_changes(self, changes: model.Delta) -> None:
        for change in changes.items:
            transitioner = self._transitioners_map.get(change.resource_type)
            if not transitioner:
                raise ValueError(f"No transitioner registered for resource type [{change.resource_type}]")
            try:
                transitioner.validate(change)
            except Exception as e:
                name = change.target.name if change.target else change.current.name
                resource_type = change.target.resource_type if change.target else change.current.resource_type
                raise ValueError(f"Invalid resource [{resource_type}.{name}] configuration: {str(e)}")

    def _transit_states(self, changes: model.Delta) -> None:
        for change in changes.items:
            assert change.target or change.current, "Missing current and/or target delta information."
            name = change.target.name if change.target else change.current.name
            transitioner = self._transitioners_map[change.resource_type]
            action = self._action_type(change)
            try:
                transitioner.apply(change)
                self._LOG.info(f"{action.capitalize()} {change.resource_type.capitalize()} [{name}] completed")
            except Exception as e:
                raise ValueError(f"{action.capitalize()} {change.resource_type.capitalize()} "
                                 f"[{name}] error: {str(e)}")

    def _pretty_print(self, changes: model.Delta) -> str:
        res = ""
        for change in changes.items:
            action = self._action_type(change)
            if action == self._DELETE:
                res += f"- {action.upper()} - {change.resource_type.capitalize()} [{change.current.name}]\n"
            else:
                res += f"- {action.upper()} - {change.resource_type.capitalize()} [{change.target.name}] " \
                       f"with parameters [{change.target.params}] \n"
        return res

    def _action_type(self, change: model.DeltaItem) -> str:
        if change.deleted:
            return self._DELETE
        elif not change.current:
            return self._CREATE
        return self._UPDATE_OR_REPLACE
