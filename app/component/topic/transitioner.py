import logging
import time

from app import client, model
from app.component import component


class TopicTransitioner(component.Transitioner):
    _LOG = logging.getLogger(__name__)

    def __init__(self, *, admin_client: client.AdminClient):
        self._admin_client = admin_client

    def drop(self, spec: model.SpecItem, *, cascade: bool = False) -> None:
        if self._admin_client.topic_describe(spec.name):
            self._admin_client.topic_drop(spec.name)

    def apply(self, delta: model.DeltaItem) -> None:
        if delta.deleted:
            try:
                self._admin_client.topic_drop(delta.current.name)
            except Exception as e:
                raise ValueError(f"Error while deleting topic [{delta.current.name}]: {str(e)}")
            self._LOG.info(f"Topic [{delta.current.name}] deleted")
        else:
            assert delta.target, "Missing topic target object"
            try:
                target_params = model.TopicParams(**delta.target.params)
                if delta.current:
                    self._admin_client.topic_drop(delta.current.name)
                    for i in range(0, 5):
                        if not self._admin_client.topic_describe(delta.current.name):
                            break
                        time.sleep(0.2)
                    if self._admin_client.topic_describe(delta.current.name):
                        raise ValueError(f"Topic [{delta.current.name}] was not deleted withing the timeout")
                self._admin_client.topic_create(topic_name=delta.target.name,
                                                num_partitions=target_params.partitions,
                                                replication_factor=target_params.replicas)
            except Exception as e:
                raise ValueError(f"Error while updating topic [{delta.target.name}]: {str(e)}")
            if delta.current:
                self._LOG.info(f"Topic [{delta.target.name}] replaced")
            else:
                self._LOG.info(f"Topic [{delta.target.name}] created")

    def validate(self, delta: model.DeltaItem) -> None:
        target_params = model.TopicParams(**delta.target.params)
        if target_params.partitions <= 0 or target_params.replicas <= 0:
            raise ValueError(f"Partitions [{target_params.partitions}] "
                             f"or replicas [{target_params.replicas}] "
                             f"must be None or positive")
