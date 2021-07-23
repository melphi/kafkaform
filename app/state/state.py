import logging
from typing import Dict, List

from app import component, model


class State:
    _LOG = logging.getLogger(__name__)

    def __init__(self, components: List[component.Component]):
        self._components_map: Dict[str, component.Component] = {}
        for comp in components:
            assert comp.resource_type not in self._components_map, \
                f"Component for resource [{comp.resource_type}] already exists"
            self._components_map[comp.resource_type] = comp

    def load_current(self) -> model.Spec:
        spec = model.Spec(specs=[])
        for comp in self._components_map.values():
            for name in comp.resolver.system_list():
                spec.specs.append(comp.resolver.system_get(name))
        return spec

    def load_delta(self, target: model.Spec) -> model.Delta:
        self._check_naming(target)

        descriptions = self._get_descriptions(target)
        self._check_schema(target, descriptions)

        current = self.load_current()
        delta = self._build_delta(current, target)

        self._check_dependencies(target)
        return self._ordered_delta(delta)

    def _get_descriptions(self, target: model.Spec) -> List[model.Description]:
        descriptions = list()
        for spec in target.specs:
            try:
                description = self._components_map[spec.resource_type].resolver.describe(spec)
                descriptions.append(description)
            except Exception as e:
                raise ValueError(f"Could not describe resource [{spec.full_name()}]: {str(e)}")
        return descriptions

    def _check_naming(self, target: model.Spec) -> None:
        # TODO: Check naming convention
        # TODO: Check naming uniqueness
        pass

    def _check_schema(self, target: model.Spec, descriptions: List[model.Description]) -> None:
        schemas = self._load_schemas(target)
        for description in descriptions:
            if description.spec.schema_name:
                expected = schemas.get(description.spec.schema_name)
                if not expected:
                    raise ValueError(f"Resource [{description.spec.full_name}] "
                                     f"requires schema [{description.spec.schema_name}] which is not defined.")
                if description.schema != expected:
                    raise ValueError(f"Resource [{description.spec.full_name}] schema mismatch. "
                                     f"Expected [{expected}], actual [{description.schema}].")

    def _load_schemas(self, target: model.Spec) -> Dict[str, model.SchemaParams]:
        schemas: Dict[str, model.SchemaParams] = {}
        for spec in target.specs:
            if spec.resource_type == model.RESOURCE_SCHEMA:
                resolved = self._components_map[model.RESOURCE_SCHEMA].resolver.system_get(spec.name)
                if resolved:
                    described = self._components_map[model.RESOURCE_SCHEMA].resolver.describe(resolved)
                else:
                    described = self._components_map[model.RESOURCE_SCHEMA].resolver.describe(spec)
                schemas[spec.name] = described.schema
        return schemas

    def _check_dependencies(self, target: model.Spec) -> None:
        # TODO Connector checks for connector plugins
        # TODO Stream and Table checks for UDFs
        pass
    
    def _ordered_delta(self, delta: model.Delta) -> model.Delta:
        # TODO Check ordering
        #  - Connectors first
        #  - For now, tables and then stream. Later stream and tables use a queue for dependencies
        #  - Sink last
        pass

    def _build_delta(self, current: model.Spec, target: model.Spec) -> model.Delta:
        # System can have multiple items with the same name but different types.
        current_map: Dict[str, List[model.SpecItem]] = {}
        for spec in current.specs:
            if spec.name in current_map:
                current_map[spec.name].append(spec)
            else:
                current_map[spec.name] = [spec]

        delta = model.Delta(items=[])
        for target_spec in target.specs:
            found = False
            for current_item in current_map.get(target_spec.name):
                if current_item.resource_type == target_spec.resource_type:
                    found = True
                    resolver = self._components_map[target_spec.resource_type].resolver
                    if resolver.equals(current_item, target_spec):
                        self._LOG.info(f"{target_spec.resource_type} [{target_spec.name}] changes")
                        delta.items.append(model.DeltaItem(
                            deleted=False,
                            type=target_spec.resource_type,
                            current=current_item,
                            target=target_spec))
                    else:
                        self._LOG.info(f"{target_spec.resource_type} [{target_spec.name}] remains the same")
            if not found:
                self._LOG.info(f"{target_spec.resource_type} [{target_spec.name}] is new")
                delta.items.append(model.DeltaItem(
                    deleted=False,
                    type=target_spec.resource_type,
                    current=None,
                    target=target_spec))
        return delta
