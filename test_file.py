import unittest

tescart = __import__('tesc-art')



class TestFileLoading(unittest.TestCase):
    def test_missing_file(self):
        data = tescart.parse_file('nofile')
        self.assertEqual(data, [])

    def test_empty_file(self):
        data = tescart.parse_file('testdata/empty.txt')
        self.assertEqual(data, [])

    def test_file_with_only_comments(self):
        data = tescart.parse_file('testdata/only_comments.txt')
        self.assertEqual(data, [])

    def test_file_with_two_commands(self):
        data = tescart.parse_file('testdata/two_commands.txt')
        self.assertEqual(data, ['command 1', 'command 2'])

    def test_file_with_extra_whitespace(self):
        data = tescart.parse_file('testdata/extra_whitespace.txt')
        self.assertEqual(data, ['command 1', 'command 2'])

    def test_file_with_inline_comments(self):
        data = tescart.parse_file('testdata/inline_comments.txt')
        self.assertEqual(data, ['valid command'])

    def test_multiple_sections(self):
        data = tescart.parse_file('testdata/multiple_sections.txt')
        self.assertEqual(data, ['one', 'two'])



class TestLoadConfig(unittest.TestCase):
    def test_empty_list(self):
        data = tescart.load_config([])
        self.assertEqual(data, {})

    def test_single_pair(self):
        data = tescart.load_config(['key value'])
        self.assertEqual(data, { 'key': 'value' })

    def test_single_word(self):
        data = tescart.load_config(['word'])
        self.assertEqual(data, {})

    def test_multiple_words(self):
        data = tescart.load_config(['one two three four'])
        self.assertEqual(data, { 'one': 'two three four' })



if __name__ == '__main__':
    unittest.main()
