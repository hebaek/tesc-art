# Public imports
from datetime import timedelta, datetime
from random   import randrange
from copy     import deepcopy



class Event():
    def __init__(self, data):
        if not 'cmd' in data: data['cmd'] = 'noop'

        if 'cmd'    in data: self.cmd    = data['cmd']
        if 'target' in data: self.target = data['target']
        if 'params' in data: self.params = data['params']






class ChainEvent(Event):
    def __init__(self, data):
        if not 'delay'  in data: data['delay']  = {'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 }
        if not 'random' in data: data['random'] = {'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'microseconds': 0 }

        super().__init__(data)

        if 'delay'  in data: self.delay  = data['delay' ]
        if 'random' in data: self.random = data['random']



    def getdelay(self):
        delay = {}
        for e in ['days', 'hours', 'minutes', 'seconds', 'microseconds']:
            delay[e] = self.delay[e] + randrange(-self.random[e], self.random[e] + 1)

        return timedelta(days=delay['days'], hours=delay['hours'], minutes=delay['minutes'], seconds=delay['seconds'], microseconds=delay['microseconds'])






class ScheduleEvent(Event):
    def __init__(self, data):
        if not 'time' in data: data['time'] = { 'type': 'none' }

        super().__init__(data)

        if 'time' in data: self.time = data['time']
        self.active = True



    def test_time(self, testtime):
        if self.time['type'] == 'boot':
            self.time['type'] = 'booted'
            return True



        elif self.time['type'] == 'date':
            temptime = deepcopy(self.time)
            eventtime = datetime(
                temptime['Y'] if temptime['Y'] else testtime.Y,
                temptime['M'] if temptime['M'] else testtime.M,
                temptime['D'] if temptime['D'] else testtime.D,
                temptime['h'] if temptime['h'] else testtime.h,
                temptime['m'] if temptime['m'] else testtime.m,
                temptime['s'] if temptime['s'] else testtime.s,
            )

            if self.active == False and eventtime < testtime.replace(microsecond=0):
                self.active = True

            elif self.active == True and eventtime == testtime.replace(microsecond=0):
                self.active = False
                return True



        elif self.time['type'] == 'weekday':
            if self.time['weekday'] != testtime.weekday(): return False

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
