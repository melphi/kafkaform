import logging

from app import client, model


class Actioner:
    """Performs system state transit actions"""

    _LOG = logging.getLogger(__name__)

    def __init__(self,
                 connect_client: client.ConnectClient,
                 ksql_client: client.KsqlClient):
        self._connect_client = connect_client
        self._ksql_client = ksql_client

    def transit_state(self, changes: model.DeltaState, ask_confirmation: bool) -> None:
        assert not changes.delta_sinks, "Delta sinks not yet supported"
        if ask_confirmation:
            self._LOG.info("Planned changes..")
            self._LOG.info(self._pretty_print(changes))
            choice = input("Confirm changes? [Y/n]\n")
            print()
            if choice != "Y":
                self._LOG.warning("Operation aborted")
                exit(1)
        self._transit_states(changes)

    def _transit_states(self, changes: model.DeltaState) -> None:
        for delta in changes.delta_sources:
            self._transit_source_state(delta)
        for delta in changes.delta_tables:
            self._transit_table_state(delta)
        for stream in changes.delta_streams:
            self._transit_stream_state(stream)

    def _pretty_print(self, delta: model.DeltaState) -> str:
        assert not delta.delta_sinks, "delta sinks not yet supported"
        res = ""
        if delta.delta_sources:
            res += "Source connectors changes: \n"
            for item in delta.delta_sources:
                if item.deleted:
                    res += self._pretty_delete("Source connector", item.current.name)
                else:
                    res += self._pretty_update(
                        "Source connector", item.target.name, item.target.config, not item.current)
        if delta.delta_streams:
            res += "Streams changes: \n"
            for item in delta.delta_streams:
                if item.deleted:
                    res += self._pretty_delete("Stream", item.current.name)
                else:
                    res += self._pretty_update("Stream", item.target.name, item.target.sql, not item.current)
        else:
            res += "Source connectors remain the same\n"
        return res

    def _transit_source_state(self, change: model.SourceDeltaState):
        if change.deleted:
            try:
                self._connect_client.connector_delete(change.current.name)
            except Exception as e:
                raise ValueError(f"Error while deleting source connector [{change.current.name}]: {str(e)}")
            self._LOG.info(f"Source connector [{change.current.name}] deleted")
        else:
            assert change.target, "Missing connector target object"
            try:
                self._connect_client.connector_update(change.target.name, change.target.config)
            except Exception as e:
                raise ValueError(f"Error while updating source connector [{change.target.name}]: {str(e)}")
            if change.current:
                self._LOG.info(f"Source connector [{change.target.name}] updated")
            else:
                self._LOG.info(f"Source connector [{change.target.name}] created")

    def _transit_table_state(self, change: model.TableDeltaState):
        if change.deleted:
            try:
                self._ksql_client.table_drop(change.current.name)
            except Exception as e:
                raise ValueError(f"Error while deleting table [{change.current.name}]: {str(e)}")
            self._LOG.info(f"Table [{change.current.name}] deleted")
        else:
            assert change.target, "Missing table target object"
            try:
                self._ksql_client.execute_command(change.target.sql)
            except Exception as e:
                raise ValueError(f"Error while updating table [{change.target.name}]: {str(e)}")
            if change.current:
                self._LOG.info(f"Table [{change.target.name}] updated")
            else:
                self._LOG.info(f"Table [{change.target.name}] created")

    def _transit_stream_state(self, change: model.StreamDeltaState):
        if change.deleted:
            try:
                self._ksql_client.stream_drop(change.current.name)
            except Exception as e:
                raise ValueError(f"Error while deleting stream [{change.current.name}]: {str(e)}")
            self._LOG.info(f"Stream [{change.current.name}] deleted")
        else:
            assert change.target, "Missing stream target object"
            try:
                self._ksql_client.execute_command(change.target.sql)
            except Exception as e:
                raise ValueError(f"Error while updating stream [{change.target.name}]: {str(e)}")
            if change.current:
                self._LOG.info(f"Stream [{change.target.name}] updated")
            else:
                self._LOG.info(f"Stream [{change.target.name}] created")

    def _pretty_delete(self, resource_type: str, name: str) -> str:
        return f"- DELETE - {resource_type} [{name}]\n"

    def _pretty_update(self, resource_type: str, name: str, config: any, is_new: bool) -> str:
        if is_new:
            return f"- NEW - {resource_type} [{name}] with config [{config}]\n"
        return f"- UPDATE - {resource_type} [{name}] with config [{config}]\n"
