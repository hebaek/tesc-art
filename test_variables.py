import unittest

import variables



class TestParseValue(unittest.TestCase):
    def test_parse_value_empty_string(self):
        data = variables.parse_value('')
        self.assertEqual(data, None)

    def test_parse_value_int_0(self):
        data = variables.parse_value(0)
        self.assertEqual(data, { 'type': 'value', 'value': 0 })

    def test_parse_value_float_0(self):
        data = variables.parse_value(0.0)
        self.assertEqual(data, { 'type': 'value', 'value': 0.0 })

    def test_parse_value_string_int_0(self):
        data = variables.parse_value('0')
        self.assertEqual(data, { 'type': 'value', 'value': 0 })

    def test_parse_value_string_float_0(self):
        data = variables.parse_value('0.0')
        self.assertEqual(data, { 'type': 'value', 'value': 0.0 })

    def test_parse_value_string_range(self):
        data = variables.parse_value('(1,2)')
        self.assertEqual(data, { 'type': 'range', 'range': (1, 2) })

    def test_parse_value_string_variable(self):
        data = variables.parse_value('x')
        self.assertEqual(data, { 'type': 'variable', 'variable': 'x' })



if __name__ == '__main__':
    unittest.main()
