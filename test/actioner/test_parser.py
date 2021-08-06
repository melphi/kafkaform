import os
import unittest

from app import actioner
from test import instances


class ParserTest(unittest.TestCase):
    def test_parse_basic(self):
        # Given
        path = os.path.join(os.path.dirname(__file__), "../resources/basic.yml")
        parser = actioner.Parser(parsers_map=instances.PARSERS_MAP)

        # When
        res = parser.parse(path)

        # Then
        self.assertTrue(res.specs)

    def test_render_advanced(self):
        # Given
        path = os.path.join(os.path.dirname(__file__), "../resources/advanced.yml")
        parser = actioner.Parser(parsers_map=instances.PARSERS_MAP)

        # When
        res = parser.render(path)

        # Then
        self.assertTrue(res)

    def test_parse_advanced(self):
        # Given
        path = os.path.join(os.path.dirname(__file__), "../resources/advanced.yml")
        parser = actioner.Parser(parsers_map=instances.PARSERS_MAP)

        # When
        res = parser.parse(path)

        # Then
        self.assertTrue(res.specs)
        for spec in res.specs:
            self.assertIsNotNone(spec.name)
            self.assertIsNotNone(spec.resource_type)
