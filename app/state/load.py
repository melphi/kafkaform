from typing import List

from app import client
from app import model


class SystemLoader:
    """Loads system resources, eg Kafka connectors, streams, external schema definition, etc."""

    def __init__(self, *, connect_client: client.ConnectClient, ksql_client: client.KsqlClient):
        self._connect_client = connect_client
        self._ksql_client = ksql_client

    def load_resources(self, target: model.Spec) -> model.Resources:
        return model.Resources(
            connector_plugins=self._connect_client.plugins_list(),
            schemas=self._load_schemas(target),
            udfs=self._ksql_client.udf_list())

    def _load_schemas(self, target: model.Spec) -> List[model.SchemaParams]:
        pass

    def _load_udfs(self) -> List[client.UdfInfo]:
        udfs = []
        for udf in self._ksql_client.udf_list():
            udfs.append(self._ksql_client.udf_describe(udf))
        return udfs



# class _ConnectorsStateLoader:
#     def __init__(self, *, connect_client: client.ConnectClient):
#         self._connect_client = connect_client
#
#     def list_plugins(self):
#         pass
#
#
# class _KsqlStateLoader:
#     def __init__(self, *, ksql_client: client.KsqlClient):
#         self._ksql_client = ksql_client




# class StateLoader:
#     """Loads the system state"""
#
#     _VALIDATORS: List[validate.Validator] = [validate.NamingConventionValidator(),
#                                              validate.NamingConsistencyValidator(),
#                                              validate.UniqueNamesValidator()]
#     _LOG = logging.getLogger(__name__)
#
#     def __init__(self, *, connect_client: client.ConnectClient, ksql_client: client.KsqlClient):
#         self._connectors_loader = _ConnectorsStateLoader(connect_client=connect_client)
#         self._ksql_loader = _KsqlStateLoader(ksql_client=ksql_client)
#
#     def load_system_delta(self, target: spec.Spec) -> delta.DeltaState:
#         assert not target.sinks, "delta sinks not yet supported"
#         self._LOG.info(f"Evaluating system delta..")
#         changes = delta.DeltaState(
#             delta_sinks=list(),
#             delta_sources=self._connectors_loader.system_sources_delta(target.sources),
#             delta_streams=self._ksql_loader.system_streams_delta(target.streams),
#             delta_tables=self._ksql_loader.system_tables_delta(target.tables))
#         self._LOG.info(f"..done\n\n")
#         self._validate(target, changes)
#         return changes
#
#     def load_system_state(self) -> spec.Spec:
#         return spec.Spec(
#             schemas=list(),
#             sinks=list(),
#             sources=self._connectors_loader.sources_state(),
#             streams=self._ksql_loader.streams_state(),
#             tables=self._ksql_loader.tables_state())
#
#     def _validate(self, target: spec.Spec, changes: delta.DeltaState) -> None:
#         # TODO: Pass System state (eg connectors) for dependencies validation.
#         errors = list()
#         for validator in self._VALIDATORS:
#             try:
#                 validator.validate(target=target, changes=changes)
#             except Exception as e:
#                 errors.append(e)
#         if errors:
#             text = "There are validation errors: "
#             for error in errors:
#                 text += f"\n-{str(error)}"
#             raise ValueError(text)
#
#
# class _ConnectorsStateLoader:
#     _LOG = logging.getLogger(__name__)
#
#     def __init__(self, *, connect_client: client.ConnectClient):
#         self._connect_client = connect_client
#
#     def sources_state(self) -> List[spec.SourceSpec]:
#         res = list()
#         for conn_name in self._connect_client.list_connectors():
#             conn = self._connect_client.get_connector(conn_name)
#             res.append(self._as_spec(conn))
#         return res
#
#     def system_sinks_delta(self, targets: List[spec.SinkSpec]) -> List[delta.SinkDeltaState]:
#         # TODO: Implement sinks delta.
#         raise NotImplementedError()
#
#     def system_sources_delta(self, targets: List[spec.SourceSpec]) -> List[delta.SourceDeltaState]:
#         # TODO: Implement deleted resources
#         changes = list()
#         for target in targets:
#             conn = self._connect_client.get_connector(target.name)
#             if not conn:
#                 self._LOG.info(f"Connector [{target.name}] is new")
#                 changes.append(self._create_delta(conn, target))
#             elif not self._source_equals(source=conn, target=target):
#                 self._LOG.info(f"Connector [{target.name}] changes")
#                 changes.append(self._create_delta(conn, target))
#             else:
#                 self._LOG.info(f"Connector [{target.name}] remains the same")
#         return changes
#
#     def _source_equals(self, *, source: client.ConnectorInfo, target: spec.SourceSpec) -> bool:
#         for key, val in target.config.items():
#             if key not in source.config or str(source.config[key]) != str(val):
#                 return False
#         return True
#
#     def _create_delta(self,  source: client.ConnectorInfo, target: spec.SourceSpec) -> delta.SourceDeltaState:
#         current = self._as_spec(source) if source else None
#         return delta.SourceDeltaState(
#             current=current,
#             deleted=False,
#             target=target)
#
#     def _as_spec(self, source: client.ConnectorInfo) -> spec.SourceSpec:
#         return spec.SourceSpec(
#             name=source.name,
#             config=source.config,
#             schema=None)
#
#
# class _KsqlStateLoader:
#     _LOG = logging.getLogger(__name__)
#
#     def __init__(self, *, ksql_client: client.KsqlClient):
#         self._ksql_client = ksql_client
#
#     def streams_state(self) -> List[spec.StreamSpec]:
#         res = list()
#         for name in self._ksql_client.stream_list():
#             info = self._ksql_client.resource_describe(name)
#             res.append(self._as_stream_spec(info))
#         return res
#
#     def system_streams_delta(self, targets: List[spec.StreamSpec]) -> List[delta.StreamDeltaState]:
#         deltas = list()
#         for target in targets:
#             info = self._ksql_client.resource_describe(target.name)
#             if not info:
#                 self._LOG.info(f"Stream [{target.name}] is new")
#                 deltas.append(self._create_stream_delta(info, target))
#             elif not self._stream_equals(source=info, target=target):
#                 self._LOG.info(f"Stream [{target.name}] changes")
#                 deltas.append(self._create_stream_delta(info, target))
#             else:
#                 self._LOG.info(f"Stream [{target.name}] remains the same")
#         return deltas
#
#     def system_tables_delta(self, targets: List[spec.TableSpec]) -> List[delta.TableDeltaState]:
#         deltas = list()
#         for target in targets:
#             info = self._ksql_client.resource_describe(target.name)
#             if not info:
#                 self._LOG.info(f"Table [{target.name}] is new")
#             elif not self._table_equals(source=info, target=target):
#                 self._LOG.info(f"Table [{target.name}] changes")
#                 deltas.append(self._create_table_delta(info, target))
#             else:
#                 self._LOG.info(f"Table [{target.name}] remains the same")
#         return deltas
#
#     def tables_state(self) -> List[spec.TableSpec]:
#         res = list()
#         for name in self._ksql_client.table_list():
#             info = self._ksql_client.resource_describe(name)
#             res.append(self._as_table_spec(info))
#         return res
#
#     def _create_stream_delta(self, source: client.ResourceInfo, target: spec.StreamSpec) -> delta.StreamDeltaState:
#         current = self._as_stream_spec(source) if source else None
#         return delta.StreamDeltaState(
#             current=current,
#             deleted=False,
#             target=target)
#
#     def _create_table_delta(self, source: client.ResourceInfo, target: spec.TableSpec) -> delta.TableDeltaState:
#         current = self._as_table_spec(source) if source else None
#         return delta.TableDeltaState(
#             current=current,
#             deleted=False,
#             target=target)
#
#     def _stream_equals(self, *, source: client.ResourceInfo, target: spec.StreamSpec) -> bool:
#         assert source.sql and source.sql.strip(), "Missing source SQL"
#         assert target.sql and target.sql.strip(), "Missing target SQL"
#         return target.sql.strip() == source.sql.strip()
#
#     def _table_equals(self, *, source: client.ResourceInfo, target: spec.TableSpec) -> bool:
#         assert source.sql and source.sql.strip(), "Missing source SQL"
#         assert target.sql and target.sql.strip(), "Missing target SQL"
#         return target.sql.strip() == source.sql.strip()
#
#     def _as_stream_spec(self, source: client.ResourceInfo) -> spec.StreamSpec:
#         return spec.StreamSpec(
#             name=source.name,
#             sql=source.sql,
#             schema=None)
#
#     def _as_table_spec(self, source: client.ResourceInfo) -> spec.TableSpec:
#         return spec.TableSpec(
#             name=source.name,
#             sql=source.sql,
#             schema=None)
