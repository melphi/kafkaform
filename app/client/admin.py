from typing import List, Optional

import kafka
from kafka import admin

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
        try:
            self._admin_client = kafka.KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        except Exception as e:
            raise ValueError(f"Failed to connect to bootstrap_servers [{bootstrap_servers}]: {str(e)}")

    def topic_create(
            self, *, topic_name: str, num_partitions: int, replication_factor: int
    ) -> None:
        topic = admin.NewTopic(topic_name,
                               num_partitions=num_partitions,
                               replication_factor=replication_factor)
        self._admin_client.create_topics([topic])

    def topic_describe(self, topic_name: str) -> Optional[model.TopicInfo]:
        topics = self._admin_client.describe_topics([topic_name])
        for topic in topics:
            if topic["topic"] == topic_name:
                partitions = len(topic["partitions"])
                replicas = len(topic["partitions"][0]["replicas"])
                return model.TopicInfo(name=topic_name,
                                       partitions=partitions,
                                       replicas=replicas)
        return None

    def topic_drop(self, topic_name: str) -> None:
        self._admin_client.delete_topics([topic_name])

    def topics_list(self) -> List[str]:
        topics = self._admin_client.describe_topics()
        return [topic['topic'] for topic in topics if not topic["is_internal"]]
