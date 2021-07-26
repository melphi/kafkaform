import unittest

import tempfile
import context
import yaml

from app import command
from app import deps


class TestKafkaDumpCommand(unittest.TestCase):
    def test_run(self):
        # Given
        file_path = "resources/project/raw_de.yml"
        with tempfile.NamedTemporaryFile("w+") as target:
            # When
            with context.ITestContext() as ctx:
                dep = deps.Dependencies(ctx.get_config())

                cmd = command.KafkaApplyCommand(
                    ask_confirmation=False,
                    parser=dep.parser,
                    resolver=dep.resolver,
                    transitioner=dep.transitioner,
                    file_path=file_path)
                cmd.run()

                cmd = command.KafkaDumpCommand(
                    parser=dep.parser,
                    resolver=dep.resolver,
                    dest_path=target.name)
                cmd.run()
            written = target.read()

        # Then
        self.assertTrue(yaml.safe_load(written))
        self.assertIn("sources:", written)
        self.assertIn("streams:", written)
