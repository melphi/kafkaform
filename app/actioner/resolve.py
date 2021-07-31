import logging
from typing import Dict, List

from app import component, model
from app.actioner import validate


class Resolver:
    """Resolves system delta, validates system configuration."""

    _LOG = logging.getLogger(__name__)

    def __init__(self, *, resolvers_map: Dict[str, component.Resolver]):
        self._resolvers_map = resolvers_map
        self._validators = [
            validate.NameConventionValidator(),
            validate.NameUniquenessValidator()]

    def load_checked_delta(self, target: model.Spec) -> model.Delta:
        target_descriptions = self._get_descriptions(target)
        assert len(target_descriptions) == len(target.specs)
        self._validate_target(target_descriptions)

        current = self.load_current()
        delta = self._build_delta(current, target)

        self._check_dependencies(
            current=current, target_descriptions=target_descriptions)
        self._order_delta(delta)
        return delta

    def load_current(self) -> model.Spec:
        spec = model.Spec(specs=[])
        for resolver in self._resolvers_map.values():
            for name in resolver.system_list():
                spec.specs.append(resolver.system_get(name))
        return spec

    def _get_descriptions(self, target: model.Spec) -> List[model.Description]:
        descriptions = list()
        for spec in target.specs:
            try:
                assert spec.resource_type in self._resolvers_map, \
                    f"Resource type [{spec.resource_type}] does not have a corresponding registered resolver"
                description = self._resolvers_map[spec.resource_type].describe(spec)
                descriptions.append(description)
            except Exception as e:
                raise ValueError(f"Could not describe resource [{spec.full_name()}]: {str(e)}")
        return descriptions

    def _validate_target(self, target_descriptions: List[model.Description]) -> None:
        for validator in self._validators:
            validator.validate_target(descriptions=target_descriptions)
        self._check_schema(target_descriptions)

    def _check_schema(self, descriptions: List[model.Description]) -> None:
        schemas = self._load_schemas(descriptions)
        for description in descriptions:
            if description.spec.schema_name:
                expected = schemas.get(description.spec.schema_name)
                if not expected:
                    raise ValueError(f"Resource [{description.spec.full_name}] "
                                     f"requires schema [{description.spec.schema_name}] which is not defined.")
                # TODO: Should compare different order of elements.
                if description.schema != expected:
                    raise ValueError(f"Resource [{description.spec.full_name}] schema mismatch. "
                                     f"Expected [{expected}], actual [{description.schema}].")

    def _load_schemas(self, descriptions: List[model.Description]) -> Dict[str, model.SchemaParams]:
        schemas: Dict[str, model.SchemaParams] = {}
        for desc in descriptions:
            if desc.spec.resource_type == model.RESOURCE_SCHEMA:
                assert desc.spec.name not in schemas, f"Duplicated schema name [{desc.spec.name}]"
                schemas[desc.spec.name] = desc.schema
        return schemas

    def _check_dependencies(self, *,
                            current: model.Spec,
                            target_descriptions: List[model.Description]) -> None:
        # TODO Consider resources added or removed with delta
        # TODO Stream and Table checks for UDFs
        for desc in target_descriptions:
            for dep in desc.depends:
                found = False
                for curr in current.specs:
                    if curr.resource_type == dep.resource_type \
                            and curr.name.lower() == dep.name.lower():
                        found = True
                        break
                if not found:
                    raise ValueError(f"Resource {desc.spec.resource_type.capitalize()} [{desc.spec.name}] "
                                     f"depends on {dep.resource_type.capitalize()} [{dep.name}]"
                                     f"which was not found in the system")

    def _order_delta(self, delta: model.Delta) -> None:
        orders = {
            model.RESOURCE_TOPIC: 1,
            model.RESOURCE_SCHEMA: 2,
            model.RESOURCE_SOURCE: 3,
            model.RESOURCE_TABLE: 4,
            model.RESOURCE_STREAM: 5,
            model.RESOURCE_SINK: 6}
        tuples = list()
        for item in delta.items:
            pos = orders.get(item.resource_type)
            assert pos, f"Order position not defined for {item.resource_type}"
            tuples.append((pos, item))
        tuples = sorted(tuples, key=lambda x: x[0])
        delta.items = [item[1] for item in tuples]

    def _build_delta(self, current: model.Spec, target: model.Spec) -> model.Delta:
        # System can have multiple items with the same name but different types.
        current_map: Dict[str, List[model.SpecItem]] = {}
        for spec in current.specs:
            if spec.name in current_map:
                current_map[spec.name.lower()].append(spec)
            else:
                current_map[spec.name.lower()] = [spec]

        delta = model.Delta(items=[])
        for target_spec in target.specs:
            found = False
            if target_spec.name.lower() in current_map:
                for current_item in current_map.get(target_spec.name.lower()):
                    if current_item.resource_type == target_spec.resource_type:
                        found = True
                        resolver = self._resolvers_map[target_spec.resource_type]
                        if not resolver.equals(current_item, target_spec):
                            self._LOG.info(f"{target_spec.resource_type} [{target_spec.name}] changes")
                            delta.items.append(model.DeltaItem(
                                deleted=False,
                                resource_type=target_spec.resource_type,
                                current=current_item,
                                target=target_spec))
                        else:
                            self._LOG.info(f"{target_spec.resource_type} [{target_spec.name}] remains the same")
                        break
            if not found:
                self._LOG.info(f"{target_spec.resource_type} [{target_spec.name}] is new")
                delta.items.append(model.DeltaItem(
                    deleted=False,
                    resource_type=target_spec.resource_type,
                    current=None,
                    target=target_spec))
        return delta
