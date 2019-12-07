# Public imports
from datetime import timedelta
from random   import randrange



class Event():
    commands = [
        'quit',
        'start', 'stop', 'reset',
        'on', 'off', 'toggle', 'random',
        'read',
    ]


    def __init__(self, data):
        cmdindex = None
        for i in range(0, len(data)):
            if data[i] in Event.commands: cmdindex = i

        if cmdindex == 1: data.insert(1, '')
        if cmdindex == 0: data = ['', ''] + data

        data = data + [None, None, None, None, None][len(data):]

        self.delay  = Event.parse(data[0])
        self.random = Event.parse(data[1])
        self.cmd    = data[2]
        self.target = data[3]
        self.params = data[4]



    def parse(time):
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
