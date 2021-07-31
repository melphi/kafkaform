from typing import List, Optional

from confluent_kafka import admin

from app import model


class AdminClient:
    def topic_create(
            self, *, topic_name: str, num_partitions: int, replication_factor: int
    ) -> None:
        raise NotImplementedError()

    def topic_describe(self, topic_name: str) -> Optional[model.TopicInfo]:
        raise NotImplementedError()

    def topic_drop(self, topic_name: str) -> None:
        raise NotImplementedError()

    def topics_list(self) -> List[str]:
        raise NotImplementedError()


class AdminClientImpl(AdminClient):
    def __init__(self, *, bootstrap_servers: List[str]):
        conf = {'bootstrap.servers': bootstrap_servers}
        self._client = admin.AdminClient(conf)

    def topic_create(
            self, *, topic_name: str, num_partitions: int, replication_factor: int
    ) -> None:
        topics = admin.NewTopic(topic_name,
                                num_partitions=num_partitions,
                                replication_factor=replication_factor)
        self._client.create_topics(topics)

    def topic_describe(self, topic_name: str) -> Optional[model.TopicInfo]:
        metadata = self._client.list_topics(topic_name)
        if not metadata or not metadata.topics:
            return None
        return model.TopicInfo()

    def topic_drop(self, topic_name: str) -> None:
        self._client.delete_topics([topic_name])

    def topics_list(self) -> List[str]:
        metadata = self._client.list_topics()
        pass
