# Public imports
from datetime import timedelta, datetime
from random   import randrange
from copy     import deepcopy



class Event():
    commands = [
        'quit',
        'start', 'stop', 'reset',
        'on', 'off', 'toggle', 'random',
        'set', 'read', 'react',
        'add', 'sub', 'inc', 'dec',
    ]

    weekdays = [
        'mondays',
        'tuesdays',
        'wednesdays',
        'thursdays',
        'fridays',
        'saturdays',
        'sundays',
    ]

    def __init__(self, data):
        self.cmd    = 'noop'
        self.target = None
        self.params = None

        if 'cmd' in data and data['cmd'] in Event.commands:
            self.cmd = data['cmd']

        if 'target' in data: self.target = data['target']
        if 'params' in data: self.params = data['params']






class ChainEvent(Event):
    def __init__(self, data):
        super().__init__(data)

        self.delay  = { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 }
        self.random = { 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 }

        if 'delay'  in data: self.delay  = data['delay' ]
        if 'random' in data: self.random = data['random']



    def getdelay(self):
        delay = {}
        for e in ['days', 'hours', 'minutes', 'seconds', 'microseconds']:
            delay[e] = self.delay[e] + randrange(-self.random[e], self.random[e] + 1)

        return timedelta(days=delay['days'], hours=delay['hours'], minutes=delay['minutes'], seconds=delay['seconds'], microseconds=delay['microseconds'])






class ScheduleEvent(Event):
    def __init__(self, data):
        super().__init__(data)

        self.time = { 'type': 'none' }
        self.active = False

        if 'time' in data:
            self.time = data['time']
            self.active = True



    def test_time(self, testtime):
        if self.time['type'] == 'boot':
            self.time['type'] = 'booted'
            return True



        elif self.time['type'] == 'time':
            temptime = deepcopy(self.time)
            eventtime = datetime(
                testtime.year,
                testtime.month,
                testtime.day,
                temptime['hour'  ] if isinstance(temptime['hour'  ], int) else testtime.hour,
                temptime['minute'] if isinstance(temptime['minute'], int) else testtime.minute,
                temptime['second'] if isinstance(temptime['second'], int) else testtime.second,
            )

            if self.active == False and eventtime < testtime.replace(microsecond=0):
                self.active = True

            elif self.active == True and eventtime == testtime.replace(microsecond=0):
                self.active = False
                return True



        elif self.time['type'] == 'date':
            temptime = deepcopy(self.time)
            eventtime = datetime(
                temptime['year'  ] if isinstance(temptime['year'  ], int) else testtime.year,
                temptime['month' ] if isinstance(temptime['month' ], int) else testtime.month,
                temptime['day'   ] if isinstance(temptime['day'   ], int) else testtime.day,
                temptime['hour'  ] if isinstance(temptime['hour'  ], int) else testtime.hour,
                temptime['minute'] if isinstance(temptime['minute'], int) else testtime.minute,
                temptime['second'] if isinstance(temptime['second'], int) else testtime.second,
            )

            if self.active == False and eventtime < testtime.replace(microsecond=0):
                self.active = True

            elif self.active == True and eventtime == testtime.replace(microsecond=0):
                self.active = False
                return True



        elif self.time['type'] == 'weekday':
            if self.time['weekday'] not in Event.weekdays: return False
            if self.time['weekday'] != Event.weekdays[testtime.weekday()]: return False

            temptime = deepcopy(self.time)
            eventtime = datetime(
                testtime.year,
                testtime.month,
                testtime.day,
                temptime['hour'  ] if isinstance(temptime['hour'  ], int) else testtime.hour,
                temptime['minute'] if isinstance(temptime['minute'], int) else testtime.minute,
                temptime['second'] if isinstance(temptime['second'], int) else testtime.second,
            )

            if self.active == False and eventtime < testtime.replace(microsecond=0):
                self.active = True

            elif self.active == True and eventtime == testtime.replace(microsecond=0):
                self.active = False
                return True



        return False
