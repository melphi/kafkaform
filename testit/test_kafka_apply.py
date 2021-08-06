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
                parser=dep.parser,
                resolver=dep.resolver,
                transitioner=dep.transitioner,
                file_path=file_path)
            delta = cmd.run()

        # Then
        self.assertTrue(delta)
        self.assertTrue(delta.items)

    def test_apply_idempotent(self):
        # Given
        file_path = "resources/project/raw_de.yml"

        # When
        with context.ITestContext() as ctx:
            dep = deps.Dependencies(ctx.get_config())
            cmd = command.KafkaApplyCommand(
                ask_confirmation=False,
                parser=dep.parser,
                resolver=dep.resolver,
                transitioner=dep.transitioner,
                file_path=file_path)
            delta_1 = cmd.run()
            delta_2 = cmd.run()

        # Then
        self.assertTrue(delta_1.items)
        self.assertFalse(delta_2.items)
        self.assertNotEqual(delta_1, delta_2)
