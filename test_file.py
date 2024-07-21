import unittest

import file



class TestParseFile(unittest.TestCase):
    def test_parse_file_missing_file(self):
        data = file.parse_file('nofile')
        self.assertEqual(data, [])

    def test_parse_file_empty_file(self):
        data = file.parse_file('testdata/empty.txt')
        self.assertEqual(data, [])

    def test_parse_file_file_with_only_comments(self):
        data = file.parse_file('testdata/only_comments.txt')
        self.assertEqual(data, [])

    def test_parse_file_file_with_two_commands(self):
        data = file.parse_file('testdata/two_commands.txt')
        self.assertEqual(data, ['command 1', 'command 2'])

    def test_parse_file_file_with_extra_whitespace(self):
        data = file.parse_file('testdata/extra_whitespace.txt')
        self.assertEqual(data, ['command 1', 'command 2'])

    def test_parse_file_file_with_inline_comments(self):
        data = file.parse_file('testdata/inline_comments.txt')
        self.assertEqual(data, ['valid command'])

    def test_parse_file_multiple_sections(self):
        data = file.parse_file('testdata/multiple_sections.txt')
        self.assertEqual(data, ['one', 'two'])



class TestLoadConfig(unittest.TestCase):
    def test_load_config_empty_list(self):
        data = file.load_config([])
        self.assertEqual(data, {})

    def test_load_config_single_pair(self):
        data = file.load_config(['key value'])
        self.assertEqual(data, { 'key': 'value' })

    def test_load_config_single_word(self):
        data = file.load_config(['word'])
        self.assertEqual(data, {})

    def test_load_config_multiple_words(self):
        data = file.load_config(['one two three four'])
        self.assertEqual(data, { 'one': 'two three four' })



class TestLoadEvents(unittest.TestCase):
    def test_load_events_empty_list(self):
        data = file.load_events([])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [],
            'chains':     {},
        })

    def test_load_events_interrupts_correct(self):
        data = file.load_events(['interrupts:', 'name on target params'])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [{ 'name': 'name', 'cmd': 'on', 'target': 'target', 'params': 'params' }],
            'schedule':   [],
            'chains':     {},
        })

    def test_load_events_schedule_boot_correct(self):
        data = file.load_events(['schedule:', 'boot on target params'])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [{ 'time': { 'type': 'boot' }, 'cmd': 'on', 'target': 'target', 'params': 'params' }],
            'chains':     {},
        })

    def test_load_events_schedule_boot_no_cmd(self):
        data = file.load_events(['schedule:', 'boot'])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [],
            'chains':     {},
        })

    def test_load_events_schedule_time_correct(self):
        data = file.load_events(['schedule:', '11:22:33 on target params'])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [{ 'time': { 'type': 'time', 'h': 11, 'm': 22, 's': 33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' }],
            'chains':     {},
        })

    def test_load_events_schedule_time_incomplete(self):
        data = file.load_events(['schedule:', '11:22 on target params'])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [],
            'chains':     {},
        })

    def test_load_events_schedule_time_excessive(self):
        data = file.load_events(['schedule:', '11:22:33:44 on target params'])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [],
            'chains':     {},
        })

    def test_load_events_schedule_time_wrong(self):
        data = file.load_events(['schedule:',
            '-1:22:33 on target params',
            'xx:22:33 on target params',
              ':22:33 on target params',
            '24:22:33 on target params',
            '11:-1:33 on target params',
            '11:xx:33 on target params',
              '11::33 on target params',
            '11:60:33 on target params',
            '11:22:-1 on target params',
            '11:22:xx on target params',
            '11:22:   on target params',
            '11:22:60 on target params',
        ])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [
                { 'time': { 'type': 'time', 'h': None, 'm':   22, 's':   33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h': None, 'm':   22, 's':   33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h': None, 'm':   22, 's':   33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h': None, 'm':   22, 's':   33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h':   11, 'm': None, 's':   33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h':   11, 'm': None, 's':   33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h':   11, 'm': None, 's':   33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h':   11, 'm': None, 's':   33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h':   11, 'm':   22, 's': None }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h':   11, 'm':   22, 's': None }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h':   11, 'm':   22, 's': None }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'time', 'h':   11, 'm':   22, 's': None }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
            ],
            'chains':     {},
        })

    def test_load_events_schedule_weekday_correct(self):
        data = file.load_events(['schedule:', 'mondays/11:22:33 on target params'])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [{ 'time': { 'type': 'weekday', 'weekday': 'mondays', 'h': 11, 'm': 22, 's': 33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' }],
            'chains':     {},
        })

    def test_load_events_schedule_date_correct(self):
        data = file.load_events(['schedule:', '2024-01-02/11:22:33 on target params'])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [{ 'time': { 'type': 'date', 'Y': 2024, 'M': 1, 'D': 2, 'h': 11, 'm': 22, 's': 33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' }],
            'chains':     {},
        })

    def test_load_events_schedule_date_wrong(self):
        data = file.load_events(['schedule:',
            '2024-13-02/11:22:33 on target params',
            '2024-xx-02/11:22:33 on target params',
              '2024--02/11:22:33 on target params',
            '2024-01-32/11:22:33 on target params',
            '2024-01-xx/11:22:33 on target params',
              '2024-01-/11:22:33 on target params',
        ])
        self.assertEqual(data, {
            'variables':  {},
            'interrupts': [],
            'schedule':   [
                { 'time': { 'type': 'date', 'Y': 2024, 'M': None, 'D':    2, 'h': 11, 'm': 22, 's': 33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'date', 'Y': 2024, 'M': None, 'D':    2, 'h': 11, 'm': 22, 's': 33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'date', 'Y': 2024, 'M': None, 'D':    2, 'h': 11, 'm': 22, 's': 33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'date', 'Y': 2024, 'M':    1, 'D': None, 'h': 11, 'm': 22, 's': 33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'date', 'Y': 2024, 'M':    1, 'D': None, 'h': 11, 'm': 22, 's': 33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
                { 'time': { 'type': 'date', 'Y': 2024, 'M':    1, 'D': None, 'h': 11, 'm': 22, 's': 33 }, 'cmd': 'on', 'target': 'target', 'params': 'params' },
            ],
            'chains':     {},
        })



class TestParseTimestring(unittest.TestCase):
    def test_parse_timestring_empty_string(self):
        data = file.parse_timestring('')
        self.assertEqual(data, {})

    def test_parse_timestring_bad_month(self):
        data = file.parse_timestring('2024-13-02/11:22:33')
        self.assertEqual(data, { 'type': 'date', 'Y': 2024, 'M': None, 'D': 2, 'h': 11, 'm': 22, 's': 33 })



class TestParseDelaystring(unittest.TestCase):
    def test_parse_delaystring_empty_string(self):
        data = file.parse_delaystring('')
        self.assertEqual(data, { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 })

    def test_parse_delaystring_full_string(self):
        data = file.parse_delaystring('1:2:3:4.5')
        self.assertEqual(data, { 'days': 1, 'hours': 2, 'minutes': 3, 'seconds': 4, 'microseconds': 500000 })

    def test_parse_delaystring_only_days(self):
        data = file.parse_delaystring('1:::')
        self.assertEqual(data, { 'days': 1, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 })

    def test_parse_delaystring_only_hours(self):
        data = file.parse_delaystring('2::')
        self.assertEqual(data, { 'days': 0, 'hours': 2, 'minutes': 0, 'seconds': 0, 'microseconds': 0 })

    def test_parse_delaystring_only_minutes(self):
        data = file.parse_delaystring('3:')
        self.assertEqual(data, { 'days': 0, 'hours': 0, 'minutes': 3, 'seconds': 0, 'microseconds': 0 })

    def test_parse_delaystring_only_seconds(self):
        data = file.parse_delaystring('4')
        self.assertEqual(data, { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 4, 'microseconds': 0 })

    def test_parse_delaystring_only_microseconds(self):
        data = file.parse_delaystring('.5')
        self.assertEqual(data, { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 500000 })



if __name__ == '__main__':
    unittest.main()
