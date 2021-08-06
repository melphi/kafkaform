import unittest

from app import command, deps, conf


class TestConfigDebugCommand(unittest.TestCase):
    def test_run(self):
        # Given
        file_path = "resources/project/raw_de.yml"
        dep = deps.Dependencies(conf.Config(
            kafka_connect_url="unused",
            kafka_ksql_url="unused",
            kafka_bootstrap_server="unused"))

        # When
        cmd = command.ConfigDebugCommand(
            file_path=file_path,
            parser=dep.parser)
        rendered = cmd.run()

        # Then
        self.assertIn("sources:", rendered)
        self.assertIn("streams:", rendered)

