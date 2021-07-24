from app import spec

import os
import unittest


class ParserTest(unittest.TestCase):
    def test_parse_basic(self):
        # Given
        path = os.path.join(os.path.dirname(__file__), "../resources/basic.yml")
        parser = spec.Parser()

        # When
        res = parser.parse(path)

        # Then
        self.assertIsNotNone(res)
        self.assertTrue(res.schemas)
        self.assertTrue(res.sources)
        self.assertTrue(res.streams)
        self.assertTrue(res.tables)

    def test_render_advanced(self):
        # Given
        path = os.path.join(os.path.dirname(__file__), "../resources/advanced.yml")
        parser = spec.Parser()

        # When
        res = parser.render(path)

        # Then
        self.assertIsNotNone(res)

    def test_parse_advanced(self):
        # Given
        path = os.path.join(os.path.dirname(__file__), "../resources/advanced.yml")
        parser = spec.Parser()

        # When
        res = parser.parse(path)

        # Then
        self.assertTrue(res)
        self.assertEqual(1, len(res.sources))
        for source in res.sources:
            self.assertIsNotNone(source.name)
            self.assertGreaterEqual(len(source.config), 1)

    def test_missing_schema(self):
        self.fail("Not yet implemented")
