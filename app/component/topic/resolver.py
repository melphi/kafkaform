import dataclasses
from typing import Optional, List

from app import client, component, model


class TopicResolver(component.Resolver):
    def __init__(self, *, admin_client: client.AdminClient):
        self._admin_client = admin_client

    def equals(self, current: model.SpecItem, target: model.SpecItem) -> bool:
        if current.resource_type != target.resource_type:
            return False
        current_params = model.TopicParams(**current.params)
        target_params = model.TopicParams(**target.params)
        if target_params.replicas and target_params.replicas != current_params.replicas \
                or target_params.partitions and target_params.partitions != current_params.partitions:
            return False
        return current.name.lower() == target.name.lower()

    def describe(self, target: model.SpecItem) -> model.Description:
        return model.Description(depends=[], schema=None, spec=target)

    def system_list(self) -> List[str]:
        return self._admin_client.topics_list()

    def system_get(self, name: str) -> Optional[model.SpecItem]:
        info = self._admin_client.topic_describe(name)
        if not info:
            return None
        params = model.TopicParams(partitions=info.partitions, replicas=info.replicas)
        return model.SpecItem(
            name=info.name,
            params=dataclasses.asdict(params),
            resource_type=model.RESOURCE_TOPIC,
            schema_name=None)
