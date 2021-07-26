import unittest

import context

from app import command
from app import deps


class TestKafkaPlanCommand(unittest.TestCase):
    def test_run(self):
        # Given
        file_path = "resources/project/raw_de.yml"

        # When
        with context.ITestContext() as ctx:
            dep = deps.Dependencies(ctx.get_config())
            cmd = command.KafkaPlanCommand(
                parser=dep.parser,
                resolver=dep.resolver,
                file_path=file_path)
            delta = cmd.run()

        # Then
        self.assertIsNotNone(delta)
        self.assertTrue(delta.items)
