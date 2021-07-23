import unittest

import context

from app import command
from app import deps


class TestKafkaApplyCommand(unittest.TestCase):
    def test_apply(self):
        # Given
        file_path = "resources/project/raw_de.yml"

        # When
        with context.ITestContext() as ctx:
            dep = deps.Dependencies(ctx.get_config())
            cmd = command.KafkaApplyCommand(
                ask_confirmation=False,
                connect_client=dep.connect_client,
                ksql_client=dep.ksql_client,
                file_path=file_path)
            delta = cmd.run()

        # Then
        self.assertIsNotNone(delta)
        self.assertTrue(delta.delta_sources)
        self.assertTrue(delta.delta_streams)

    def test_apply_idempotent(self):
        # Given
        file_path = "resources/project/raw_de.yml"

        # When
        with context.ITestContext() as ctx:
            dep = deps.Dependencies(ctx.get_config())
            cmd = command.KafkaApplyCommand(
                ask_confirmation=False,
                connect_client=dep.connect_client,
                ksql_client=dep.ksql_client,
                file_path=file_path)
            delta_1 = cmd.run()
            delta_2 = cmd.run()

        # Then
        self.assertNotEqual(delta_1, delta_2)
        self.assertIsNotNone(delta_2)
        self.assertFalse(delta_2.delta_sources)
        self.assertFalse(delta_2.delta_streams)
