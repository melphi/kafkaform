import unittest

import tempfile
import context
import yaml

from app import command
from app import deps


class TestKafkaDumpCommand(unittest.TestCase):
    def test_run(self):
        # Given
        with tempfile.NamedTemporaryFile("w+") as target:
            # When
            with context.ITestContext() as ctx:
                dep = deps.Dependencies(ctx.get_config())
                cmd = command.KafkaDumpCommand(
                    connect_client=dep.connect_client,
                    ksql_client=dep.ksql_client,
                    dest_path=target.name)
                cmd.run()
            written = target.read()

        # Then
        self.assertTrue(written)
        self.assertTrue(yaml.safe_load(written))
        self.assertIn("sources:", written)
        self.assertIn("streams:", written)
