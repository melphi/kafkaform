import unittest

from app import model
from app.component import stream
from test import mock


class TestStreamResolver(unittest.TestCase):
    def test_equals(self):
        # Given
        current = model.SpecItem(name="test",
                                 resource_type=model.RESOURCE_STREAM,
                                 schema_name=None,
                                 params={"sql": "CREATE STREAM refined__stream__gdp__user__v1 ( userid VARCHAR KEY,\n"
                                                "regionid VARCHAR) WITH (KAFKA_TOPIC=\'raw__source__gdp__user__v1\', "
                                                "KEY_FORMAT=\'KAFKA\' , VALUE_FORMAT = \'AVRO\', PARTITIONS=2, "
                                                "REPLICAS=1)"})
        target = model.SpecItem(name="test",
                                resource_type=model.RESOURCE_STREAM,
                                schema_name=None,
                                params={"sql": "CREATE STREAM REFINED__STREAM__GDP__USER__V1 (USERID VARCHAR KEY, "
                                               "REGIONID VARCHAR) WITH (KAFKA_TOPIC=\'raw__source__gdp__user__v1\', "
                                               "KEY_FORMAT=\'KAFKA\', PARTITIONS=2, REPLICAS=1, "
                                               "VALUE_FORMAT=\'AVRO\');"})
        resolver = stream.StreamResolver(ksql_client=mock.MockKsqlClient())

        # When
        equals = resolver.equals(current=current, target=target)

        # Then
        self.assertTrue(equals)

    def test_equals2(self):
        # Given
        current = model.SpecItem(name="test",
                                resource_type=model.RESOURCE_STREAM,
                                schema_name=None,
                                params={"sql": "CREATE STREAM refined__stream__gdp__user__v1 ( userid VARCHAR KEY,\n"
                                                "regionid VARCHAR) WITH (KAFKA_TOPIC=\'raw__source__gdp__user__v1\', "
                                                "KEY_FORMAT=\'KAFKA\' , VALUE_FORMAT = \'AVRO\', PARTITIONS=2, "
                                                "REPLICAS=1) AS SELECT (something) from table;"})
        target = model.SpecItem(name="test",
                                resource_type=model.RESOURCE_STREAM,
                                schema_name=None,
                                params={"sql": "CREATE STREAM REFINED__STREAM__GDP__USER__V1 (USERID VARCHAR KEY, "
                                            "REGIONID VARCHAR) WITH (KAFKA_TOPIC=\'raw__source__gdp__user__v1\', "
                                            "KEY_FORMAT=\'KAFKA\', PARTITIONS=2, REPLICAS=1, "
                                            "VALUE_FORMAT=\'AVRO\') AS SELECT (something) from table;"})
        resolver = stream.StreamResolver(ksql_client=mock.MockKsqlClient())

        # When
        equals = resolver.equals(current=current, target=target)

        # Then
        self.assertTrue(equals)    

    @unittest.skip("Version 6.2 not yet supported.")
    def test_equals_62(self):
        # Given
        current = model.SpecItem(name="test",
                                 resource_type=model.RESOURCE_STREAM,
                                 schema_name=None,
                                 params={"sql": "CREATE STREAM refined__stream__gdp__user__v1 (userid VARCHAR KEY, "
                                                "regionid VARCHAR) WITH (KAFKA_TOPIC=\'raw__source__gdp__user__v1\', "
                                                "PARTITIONS=2, REPLICAS=1, VALUE_FORMAT=\'AVRO\')"})
        target = model.SpecItem(name="test",
                                resource_type=model.RESOURCE_STREAM,
                                schema_name=None,
                                params={"sql": "CREATE STREAM REFINED__STREAM__GDP__USER__V1 (USERID STRING KEY, "
                                               "REGIONID STRING) WITH (KAFKA_TOPIC=\'raw__source__gdp__user__v1\', "
                                               "KEY_FORMAT=\'KAFKA\', PARTITIONS=2, REPLICAS=1, "
                                               "VALUE_FORMAT=\'AVRO\');"})
        resolver = stream.StreamResolver(ksql_client=mock.MockKsqlClient())

        # When
        equals = resolver.equals(current=current, target=target)

        # Then
        self.assertTrue(equals)
