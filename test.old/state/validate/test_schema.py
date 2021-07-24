import unittest


class TestResourceSchemaValidator(unittest.TestCase):
    def test_valid_stream(self):
        # # Given
        # validator = schema.ResourceSchemaValidator()
        # data = spec.SchemaSpec(name="test_schema", fields=[spec.FieldSpec(name="id", type=spec.FieldType.INT)])
        # target = dto.create_spec(stream=spec.StreamSpec(
        #     name="test",
        #     sql="test",
        #     schema=data))
        #
        # # When
        # try:
        #     validator.validate(target=target, delta=state.EMPTY_DELTA)
        # # Then
        #     self.fail("Exception expected")
        # except ValueError as e:
        #     self.assertFalse(str(e))

        self.fail()

    def test_valid_table(self):
        self.fail()

    def test_invalid_stream(self):
        self.fail()

    def test_invalid_table(self):
        self.fail()
