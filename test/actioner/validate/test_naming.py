import unittest

from app import model
from app.actioner import validate


class TestNamingConventionValidator(unittest.TestCase):
    def test_valid(self):
        # Given
        validator = validate.NameConventionValidator()
        targets = {
            model.RESOURCE_SOURCE: "raw__source__gdp__s_cim_policy__v1",
            model.RESOURCE_STREAM: "raw__stream__gdp__s_cim_policy__v1",
            model.RESOURCE_TABLE: "raw__table__gdp__s_cim_policy__v1"
        }
        descriptions = []
        for key, name in targets.items():
            descriptions.append(model.Description(depends=[], schema=None, spec=model.SpecItem(
                resource_type=key,
                name=name,
                params={},
                schema_name=None
            )))

        # When
        res = validator.validate_target(descriptions=descriptions)

        # Then
        self.assertTrue(res)

    def test_invalid(self):
        # TODO: Parametrize test to check streams, tables, sinks.

        # Given
        validator = validate.NameConventionValidator()
        description = model.Description(depends=[], schema=None, spec=model.SpecItem(
                resource_type=model.RESOURCE_TOPIC,
                name="test__invalid",
                params={},
                schema_name=None))

        # When
        try:
            validator.validate_target(descriptions=[description])
            # Then
            self.fail("Exception expected")
        except ValueError as e:
            self.assertIn("test__invalid", str(e))
