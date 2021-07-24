import logging
from typing import Dict, List

from app import component, model
from app.actioner import validate

# HERE I AM, TEST AND MAKE IT RUN


class Resolver:
    """Resolves system delta, validates system configuration."""

    _LOG = logging.getLogger(__name__)

    def __init__(self, resolvers_map: Dict[str, component.Resolver]):
        self._resolvers_map = resolvers_map
        self._validators = [validate.NameConventionValidator(), validate.NameUniquenessValidator()]

    def load_current(self) -> model.Spec:
        spec = model.Spec(specs=[])
        for resolver in self._resolvers_map.values():
            for name in resolver.system_list():
                spec.specs.append(resolver.system_get(name))
        return spec

    def load_delta(self, target: model.Spec) -> model.Delta:
        self._validate_target(target)

        descriptions = self._get_descriptions(target)
        self._check_schema(target, descriptions)

        current = self.load_current()
        delta = self._build_delta(current, target)

        self._check_dependencies(target)
        self._order_delta(delta)
        return delta

    def _get_descriptions(self, target: model.Spec) -> List[model.Description]:
        descriptions = list()
        for spec in target.specs:
            try:
                description = self._resolvers_map[spec.resource_type].describe(spec)
                descriptions.append(description)
            except Exception as e:
                raise ValueError(f"Could not describe resource [{spec.full_name()}]: {str(e)}")
        return descriptions

    def _validate_target(self, target: model.Spec) -> None:
        # TODO: Review how validator works. Ideally they can be extended and disabled from configuration.
        for validator in self._validators:
            validator.validate(target)

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
                resolved = self._resolvers_map[model.RESOURCE_SCHEMA].system_get(spec.name)
                if resolved:
                    described = self._resolvers_map[model.RESOURCE_SCHEMA].describe(resolved)
                else:
                    described = self._resolvers_map[model.RESOURCE_SCHEMA].describe(spec)
                schemas[spec.name] = described.schema
        return schemas

    def _check_dependencies(self, target: model.Spec) -> None:
        # TODO Connector checks for connector plugins
        # TODO Stream and Table checks for UDFs
        pass

    def _order_delta(self, delta: model.Delta) -> None:
        orders = {
            model.RESOURCE_SCHEMA: 1,
            model.RESOURCE_SOURCE: 2,
            model.RESOURCE_TABLE: 3,
            model.RESOURCE_STREAM: 4,
            model.RESOURCE_SINK: 5
        }
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
                current_map[spec.name].append(spec)
            else:
                current_map[spec.name] = [spec]

        delta = model.Delta(items=[])
        for target_spec in target.specs:
            found = False
            for current_item in current_map.get(target_spec.name):
                if current_item.resource_type == target_spec.resource_type:
                    found = True
                    resolver = self._resolvers_map[target_spec.resource_type]
                    if resolver.equals(current_item, target_spec):
                        self._LOG.info(f"{target_spec.resource_type} [{target_spec.name}] changes")
                        delta.items.append(model.DeltaItem(
                            deleted=False,
                            resource_type=target_spec.resource_type,
                            current=current_item,
                            target=target_spec))
                    else:
                        self._LOG.info(f"{target_spec.resource_type} [{target_spec.name}] remains the same")
            if not found:
                self._LOG.info(f"{target_spec.resource_type} [{target_spec.name}] is new")
                delta.items.append(model.DeltaItem(
                    deleted=False,
                    resource_type=target_spec.resource_type,
                    current=None,
                    target=target_spec))
        return delta
