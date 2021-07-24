import unittest

from app import command


class DebugCommandTest(unittest.TestCase):
    def test_run_basic(self):
        # Given
        cmd = command.ConfigDebugCommand(file_path="resources/basic.yml")

        # When
        out = cmd.run()

        # Then
        self.assertIn("connector.class: \"io.confluent.connect.hdfs.HdfsSinkConnector\"", out)

    def test_run_advanced(self):
        # Given
        cmd = command.ConfigDebugCommand(file_path="resources/advanced.yml")

        # When
        out = cmd.run()

        # Then
        self.assertIn(
            "connector.class: \"com.github.jcustenborder.kafka.connect.spooldir.SpoolDirCsvSourceConnector\"", out)

    def test_dump(self):
        # TODO: Result of dump should be parseable (eg it exported sources but it required source)
        self.fail("Not yet implemented")
