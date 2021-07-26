from typing import Dict

import logging

from app import model
from app.component import component


class Transitioner:
    _CREATE = "create"
    _DELETE = "delete"
    _UPDATE = "update"

    """Performs system state transit actions"""

    _LOG = logging.getLogger(__name__)

    def __init__(self, *, transitioners_map: Dict[str, component.Transitioner]):
        self._transitioners_map = transitioners_map

    def transit_state(self, changes: model.Delta, ask_confirmation: bool) -> None:
        if ask_confirmation:
            self._LOG.info("Planned changes..")
            self._LOG.info(self._pretty_print(changes))
            choice = input("Confirm changes? [Y/n]\n")
            print()
            if choice != "Y":
                self._LOG.warning("Operation aborted")
                exit(1)
        self._transit_states(changes)

    def _transit_states(self, changes: model.Delta) -> None:
        for change in changes.items:
            transitioner = self._transitioners_map.get(change.resource_type)
            if not transitioner:
                raise ValueError(f"No transitioner registered for resource type [{change.resource_type}]")
            assert change.target or change.current, "Missing delta current and/or target information."
            name = change.target.name if change.target else change.current.name
            action = self._action_type(change)
            try:
                transitioner.apply(change)
                self._LOG.info(f"{change.resource_type.capitalize()} [{name}] {action} completed")
            except Exception as e:
                raise ValueError(f"Error during {action} of {change.resource_type.capitalize()} "
                                 f"[{name}]: {str(e)}")

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
        return self._CREATE
