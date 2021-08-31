import unittest

import context

from app import command
from app import deps


class TestKafkaApplyCommand(unittest.TestCase):
    def test_erase(self):
        # Given
        file_path = "resources/sample/sample_dependencies.yml"

        # When
        with context.ITestContext() as ctx:
            dep = deps.Dependencies(ctx.get_config())
            command.KafkaApplyCommand(
                ask_confirmation=False,
                parser=dep.parser,
                resolver=dep.resolver,
                transitioner=dep.transitioner,
                file_path=file_path).run()

            cmd = command.KafkaEraseCommand(
                ask_confirmation=False,
                parser=dep.parser,
                transitioner=dep.transitioner,
                file_path=file_path)
            spec = cmd.run()

        # Then
        self.assertTrue(spec)
        self.assertTrue(spec.specs)
