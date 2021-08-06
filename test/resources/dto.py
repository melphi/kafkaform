from app import actioner, model


def create_delta(*,
                 current_sink: model.SinkSpec = None,
                 target_sink: model.SinkSpec = None,
                 current_source: model.SourceSpec = None,
                 target_source: model.SourceSpec = None,
                 current_stream: model.StreamSpec = None,
                 target_stream: model.StreamSpec = None,
                 current_table: model.TableSpec = None,
                 target_table: model.TableSpec = None) -> model.DeltaState:
    delta = state.DeltaState(
        delta_sinks=list(),
        delta_tables=list(),
        delta_sources=list(),
        delta_streams=list())
    if current_sink or target_sink:
        delta.delta_sinks.append(state.SinkDeltaState(deleted=False, current=current_sink, target=target_sink))
    if current_table or target_table:
        delta.delta_tables.append(state.TableDeltaState(deleted=False, current=current_table, target=target_table))
    if current_source or target_source:
        delta.delta_sources.append(state.SourceDeltaState(deleted=False, current=current_source, target=target_source))
    if current_stream or target_stream:
        delta.delta_streams.append(state.StreamDeltaState(deleted=False, current=current_stream, target=target_stream))
    if current_table or target_table:
        delta.delta_tables.append(state.TableDeltaState(deleted=False, current=current_table, target=target_table))
    return delta


def create_spec(*,
                schema: spec.SchemaSpec = None,
                sink: spec.SinkSpec = None,
                source: spec.SourceSpec = None,
                stream: spec.StreamSpec = None,
                table: spec.TableSpec = None) -> spec.Spec:
    res = spec.Spec(
        schemas=list(),
        sinks=list(),
        sources=list(),
        streams=list(),
        tables=list())
    if schema:
        res.schemas.append(schema)
    if sink:
        res.sinks.append(sink)
    if source:
        res.sources.append(source)
    if stream:
        res.sources.append(stream)
    if table:
        res.tables.append(table)
    return res
