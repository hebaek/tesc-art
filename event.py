# Public imports
from datetime import timedelta, datetime
from random   import randrange
from copy     import deepcopy



class Event():
    commands = [
        'quit',
        'start', 'stop', 'reset',
        'on', 'off', 'toggle', 'random',
        'set', 'add', 'sub', 'inc', 'dec',
        'read', 'react',
    ]



    def __init__(self, data):
        self.normalize(data)

        self.cmd    = self.data[2]
        self.target = self.data[3]
        self.params = self.data[4]



    def normalize(self, data):
        cmdindex = None
        for i in range(0, len(data)):
            if data[i] in Event.commands: cmdindex = i

        if cmdindex == 1: data.insert(1, '')
        if cmdindex == 0: data = ['', ''] + data

        self.data = data + [None, None, None, None, None][len(data):]



class ChainEvent(Event):
    def __init__(self, data):
        super().__init__(data)

        self.delay  = self.parse(self.data[0])
        self.random = self.parse(self.data[1])



    def parse(self, time):
        p = len(list(filter(lambda x: x == '.', time)))
        k = len(list(filter(lambda x: x == ':', time)))

        temp = ':'*(3-k) + time + '.'*(1-p)
        (left, u) = temp.split('.')
        values = [int(x.rjust(2, '0')) for x in left.split(':')]
        values.append(int(u.ljust(6, '0')))

        keys = ['days', 'hours', 'minutes', 'seconds', 'microseconds']
        return dict(zip(keys, values))



    def getdelay(self):
        delay = {}
        for e in ['days', 'hours', 'minutes', 'seconds', 'microseconds']:
            delay[e] = self.delay[e] + randrange(-self.random[e], self.random[e] + 1)

        return timedelta(days=delay['days'], hours=delay['hours'], minutes=delay['minutes'], seconds=delay['seconds'], microseconds=delay['microseconds'])



class ScheduleEvent(Event):
    weekdays = ['mondays', 'tuesdays', 'wednesdays', 'thursdays', 'fridays', 'saturdays', 'sundays']



    def __init__(self, data):
        super().__init__(data)

        self.type   = self.data[0]
        self.time   = self.parse(self.data[1])
        self.active = True



    def parse(self, time):
        if self.type == 'boot':
            return None



        if self.type == 'date':
            b = len(list(filter(lambda x: x == '-', time)))
            s = len(list(filter(lambda x: x == '/', time)))
            k = len(list(filter(lambda x: x == ':', time)))

            temp = '-'*(2-b) + '/'*(1-s) + ':'*(2-k) + time

            (datestring, timestring) = temp.split('/')
            (year, month, day)       = datestring.split('-')
            (hour, minute, second)   = timestring.split(':')

            return {
                'year':   int(year  ) if len(year  ) else None,
                'month':  int(month ) if len(month ) else None,
                'day':    int(day   ) if len(day   ) else None,
                'hour':   int(hour  ) if len(hour  ) else None,
                'minute': int(minute) if len(minute) else None,
                'second': int(second) if len(second) else None,
            }



        if self.type == 'day':
            (daystring, timestring) = time.split('/')

            k = len(list(filter(lambda x: x == ':', timestring)))
            temp = ':'*(2-k) + timestring
            (hour, minute, second)  = temp.split(':')

            weekday = None
            if daystring in ScheduleEvent.weekdays: weekday = ScheduleEvent.weekdays.index(daystring)

            return {
                'weekday': weekday,
                'hour':   int(hour  ) if len(hour)   else None,
                'minute': int(minute) if len(minute) else None,
                'second': int(second) if len(second) else None,
            }



    def test_time(self, testtime):
        if self.type == 'boot':
            self.type = 'booted'
            return True



        elif self.type == 'date':
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



        elif self.type == 'day':
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
