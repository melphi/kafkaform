import unittest
from app.state import validate
from app import spec
from test.resources import dto


class TestNamingConventionValidator(unittest.TestCase):
    def test_valid(self):
        # Given
        validator = validate.NamingConventionValidator()
        target_source = spec.SourceSpec(name="raw__source__gdp__s_cim_policy__v1", config={})
        target_stream = spec.StreamSpec(name="raw__stream__gdp__s_cim_policy__v1", sql="", schema=None)
        target_table = spec.TableSpec(name="raw__table__gdp__s_cim_policy__v1", sql="", schema=None)
        delta = dto.create_delta(
            target_source=target_source,
            target_stream=target_stream,
            target_table=target_table)

        # When
        res = validator.validate(target=spec.EMPTY_SPEC, delta=delta)

        # Then
        self.assertTrue(res)

    def test_invalid(self):
        # TODO: Parametrize test to check streams, tables, sinks.

        # Given
        validator = validate.NamingConventionValidator()
        target_source = spec.SourceSpec(name="test__invalid", config={})
        delta = dto.create_delta(target_source=target_source)

        # When
        try:
            validator.validate(target=spec.EMPTY_SPEC, delta=delta)
            # Then
            self.fail("Exception expected")
        except ValueError as e:
            self.assertIn("test__invalid", str(e))


class TestNamingConsistencyValidator(unittest.TestCase):
    def test_validate(self):
        self.fail()


class TestUniqueNamesValidator(unittest.TestCase):
    def test_validate(self):
        self.fail()
