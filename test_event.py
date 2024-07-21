import unittest

import datetime
import event



class TestEvent(unittest.TestCase):
    def test_event_empty_event(self):
        data = event.Event({})
        self.assertIsInstance(data, event.Event)

        self.assertFalse(hasattr(data, 'target'))
        self.assertFalse(hasattr(data, 'params'))

        self.assertEqual(data.cmd, 'noop')

    def test_event_only_cmd(self):
        data = event.Event({ 'cmd': 'cmd' })
        self.assertIsInstance(data, event.Event)

        self.assertFalse(hasattr(data, 'target'))
        self.assertFalse(hasattr(data, 'params'))

        self.assertEqual(data.cmd, 'cmd')

    def test_event_complete(self):
        data = event.Event({ 'cmd': 'cmd', 'target': 'target', 'params': 'params' })
        self.assertIsInstance(data, event.Event)

        self.assertEqual(data.cmd,    'cmd')
        self.assertEqual(data.target, 'target')
        self.assertEqual(data.params, 'params')



class TestChainEvent(unittest.TestCase):
    def test_chain_event_empty_event(self):
        data = event.ChainEvent({})
        self.assertIsInstance(data, event.Event)
        self.assertIsInstance(data, event.ChainEvent)

        self.assertTrue(hasattr(data, 'delay'))
        self.assertTrue(hasattr(data, 'random'))
        self.assertFalse(hasattr(data, 'target'))
        self.assertFalse(hasattr(data, 'params'))

        self.assertEqual(data.cmd, 'noop')
        self.assertEqual(data.getdelay(), datetime.timedelta(days=0, seconds=0, microseconds=0))

    def test_chain_event_only_cmd(self):
        data = event.ChainEvent({ 'cmd': 'cmd' })
        self.assertIsInstance(data, event.Event)
        self.assertIsInstance(data, event.ChainEvent)

        self.assertTrue(hasattr(data, 'delay'))
        self.assertTrue(hasattr(data, 'random'))
        self.assertFalse(hasattr(data, 'target'))
        self.assertFalse(hasattr(data, 'params'))

        self.assertEqual(data.cmd, 'cmd')
        self.assertEqual(data.getdelay(), datetime.timedelta(days=0, seconds=0, microseconds=0))

    def test_chain_event_only_delay_and_cmd(self):
        data = event.ChainEvent({
            'delay': { 'days': 1, 'hours': 2, 'minutes': 3, 'seconds': 4, 'microseconds': 5 },
            'cmd': 'cmd',
        })
        self.assertIsInstance(data, event.Event)
        self.assertIsInstance(data, event.ChainEvent)

        self.assertTrue(hasattr(data, 'random'))
        self.assertFalse(hasattr(data, 'target'))
        self.assertFalse(hasattr(data, 'params'))

        self.assertEqual(data.cmd,     'cmd')
        self.assertEqual(data.getdelay(), datetime.timedelta(days=1, seconds=7384, microseconds=5))

    def test_chain_event_delay_and_random_and_cmd(self):
        data = event.ChainEvent({
            'delay':  { 'days': 1, 'hours': 2, 'minutes': 3, 'seconds': 4, 'microseconds': 5 },
            'random': { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 },
            'cmd': 'cmd',
        })
        self.assertIsInstance(data, event.Event)
        self.assertIsInstance(data, event.ChainEvent)

        self.assertFalse(hasattr(data, 'target'))
        self.assertFalse(hasattr(data, 'params'))

        self.assertEqual(data.cmd,     'cmd')
        self.assertEqual(data.getdelay(), datetime.timedelta(days=1, seconds=7384, microseconds=5))




if __name__ == '__main__':
    unittest.main()
