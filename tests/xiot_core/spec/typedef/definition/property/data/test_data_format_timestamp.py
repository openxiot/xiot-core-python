import unittest

from xiot_core.spec.typedef.definition.property.data.data_format import DataFormat
from xiot_core.spec.typedef.definition.property.data.value.vtimestamp import Vtimestamp
from xiot_core.spec.typedef.definition.property.value_range import ValueRange
from xiot_core.spec.typedef.instance.property_value import PropertyValue


class TestDataFormatTimestamp(unittest.TestCase):
    def test_from_str(self) -> None:
        self.assertEqual(DataFormat.from_str("timestamp"), DataFormat.TIMESTAMP)
        self.assertEqual(str(DataFormat.TIMESTAMP), "timestamp")

    def test_class_and_types(self) -> None:
        fmt = DataFormat.TIMESTAMP
        self.assertEqual(fmt.get_java_row_name(), "long")
        self.assertEqual(fmt.get_java_class_name(), "Long")
        self.assertEqual(fmt.get_class(), Vtimestamp)
        self.assertEqual(fmt.create_object_value("1700000000000"), 1700000000000)

    def test_values(self) -> None:
        fmt = DataFormat.TIMESTAMP

        default = fmt.create_default_value()
        self.assertIsInstance(default, Vtimestamp)
        self.assertEqual(default.raw_value(), 0)

        value = fmt.create_value(1700000000000)
        self.assertIsInstance(value, Vtimestamp)
        self.assertEqual(value.raw_value(), 1700000000000)
        self.assertTrue(fmt.check(value))
        self.assertFalse(fmt.check(DataFormat.INT64.create_value(1700000000000)))

    def test_value_range(self) -> None:
        fmt = DataFormat.TIMESTAMP
        value_range = ValueRange(fmt, list_=[0, 10, 2])
        self.assertTrue(value_range.validate(fmt.create_value(8)))
        self.assertFalse(value_range.validate(fmt.create_value(9)))
        self.assertEqual(value_range.to_list(), [0, 10, 2])

    def test_property_value(self) -> None:
        fmt = DataFormat.TIMESTAMP
        property_value = PropertyValue.create(fmt)
        self.assertEqual(property_value.value.raw_value(), 0)
        property_value.update(fmt.create_value(1700000000000))
        self.assertEqual(property_value.value.raw_value(), 1700000000000)


if __name__ == "__main__":
    unittest.main()
