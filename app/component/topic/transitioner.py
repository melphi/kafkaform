from app import model
from app.component import component


class TopicTransitioner(component.Transitioner):
    def validate(self, delta: model.DeltaItem) -> None:
        raise NotImplementedError()

    def apply(self, delta: model.DeltaItem) -> None:
        # TODO: Implement topic creation code.
        # from kafka.admin import KafkaAdminClient, NewTopic
        #
        # admin_client = KafkaAdminClient(
        #     bootstrap_servers="localhost:9092",
        #     client_id='test'
        # )
        #
        # topic_list = []
        # topic_list.append(NewTopic(name="example_topic", num_partitions=1, replication_factor=1))
        # admin_client.create_topics(new_topics=topic_list, validate_only=False)
        raise NotImplementedError()
