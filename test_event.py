import unittest

import datetime
import event



class TestEvent(unittest.TestCase):
    def test_event_empty_event(self):
        data = event.Event({})
        self.assertIsInstance(data, event.Event)
        self.assertEqual(data.cmd,    'noop')
        self.assertEqual(data.target, None)
        self.assertEqual(data.params, None)

    def test_event_only_cmd(self):
        data = event.Event({ 'cmd': 'on' })
        self.assertIsInstance(data, event.Event)
        self.assertEqual(data.cmd, 'on')
        self.assertEqual(data.target, None)
        self.assertEqual(data.params, None)

    def test_event_complete(self):
        data = event.Event({ 'cmd': 'on', 'target': 'target', 'params': 'params' })
        self.assertIsInstance(data, event.Event)
        self.assertEqual(data.cmd,    'on')
        self.assertEqual(data.target, 'target')
        self.assertEqual(data.params, 'params')



class TestChainEvent(unittest.TestCase):
    def test_chain_event_empty_event(self):
        data = event.ChainEvent({})
        self.assertIsInstance(data, event.Event)
        self.assertIsInstance(data, event.ChainEvent)
        self.assertEqual(data.delay,  { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 })
        self.assertEqual(data.random, { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 })
        self.assertEqual(data.cmd,    'noop')
        self.assertEqual(data.target, None)
        self.assertEqual(data.params, None)
        self.assertEqual(data.getdelay(), datetime.timedelta(days=0, seconds=0, microseconds=0))

    def test_chain_event_only_cmd(self):
        data = event.ChainEvent({ 'cmd': 'on' })
        self.assertIsInstance(data, event.Event)
        self.assertIsInstance(data, event.ChainEvent)
        self.assertEqual(data.delay,  { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 })
        self.assertEqual(data.random, { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 })
        self.assertEqual(data.cmd,    'on')
        self.assertEqual(data.target, None)
        self.assertEqual(data.params, None)
        self.assertEqual(data.getdelay(), datetime.timedelta(days=0, seconds=0, microseconds=0))

    def test_chain_event_only_delay_and_cmd(self):
        data = event.ChainEvent({
            'delay': { 'days': 1, 'hours': 2, 'minutes': 3, 'seconds': 4, 'microseconds': 5 },
            'cmd': 'on',
        })
        self.assertIsInstance(data, event.Event)
        self.assertIsInstance(data, event.ChainEvent)
        self.assertEqual(data.delay,  { 'days': 1, 'hours': 2, 'minutes': 3, 'seconds': 4, 'microseconds': 5 })
        self.assertEqual(data.random, { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 })
        self.assertEqual(data.cmd,    'on')
        self.assertEqual(data.target, None)
        self.assertEqual(data.params, None)
        self.assertEqual(data.getdelay(), datetime.timedelta(days=1, seconds=7384, microseconds=5))

    def test_chain_event_delay_and_random_and_cmd(self):
        data = event.ChainEvent({
            'delay':  { 'days': 1, 'hours': 2, 'minutes': 3, 'seconds': 4, 'microseconds': 5 },
            'random': { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 },
            'cmd': 'on',
        })
        self.assertIsInstance(data, event.Event)
        self.assertIsInstance(data, event.ChainEvent)
        self.assertEqual(data.cmd,    'on')
        self.assertEqual(data.target, None)
        self.assertEqual(data.params, None)
        self.assertEqual(data.getdelay(), datetime.timedelta(days=1, seconds=7384, microseconds=5))




if __name__ == '__main__':
    unittest.main()
