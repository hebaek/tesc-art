# Public imports
import threading
import queue

from datetime import datetime
from time     import sleep

# Local imports
import config

from event     import Event, ChainEvent, ScheduleEvent
from variables import Variables



class Main():
    def __init__(self, hardware):
        print('main: setup')
        self.hardware   = hardware
        self.variables  = Variables()

        self.eventqueue = queue.Queue()
        self.mainthread = threading.Thread(target=self.main_thread, args=(self.eventqueue,))

        self.interrupts = None
        self.cmdqueue   = None
        self.thread     = None



    def clear(self):
        print('main: clear')
        self.eventqueue.queue.clear()

        if self.mainthread.is_alive():
            self.eventqueue.put(Event(['quit']))
            self.mainthread.join()



    def reset(self):
        print('main: reset')

        self.hardware.reset()
        self.variables.reset()

        self.eventqueue.queue.clear()

        if self.mainthread.is_alive():
            self.eventqueue.put(Event(['quit']))
            self.mainthread.join()

        self.interrupts = {}
        self.cmdqueue   = {}
        self.thread     = {}

        self.cmdqueue['_scheduler'] = queue.Queue()
        self.thread['_scheduler']   = threading.Thread(target=self.scheduler_thread, args=(self.cmdqueue['_scheduler'], self.eventqueue,))
        self.mainthread             = threading.Thread(target=self.main_thread, args=(self.eventqueue,))



    def load(self, filename):
        print('main: load')

        lines  = []

        try:
            with open(filename) as f:
                filedata = f.read()
                lines = [line for line in filedata.split('\n') if len(line) > 1 and line[0] != '#']

        except Exception:
            print('Can\'t open events file!')


        context, chain = None, None
        for line in lines:
            words = line.split()

            if   words[0] == 'variables:':  (context, chain) = ('variables',  None)
            elif words[0] == 'interrupts:': (context, chain) = ('interrupts', None)
            elif words[0] == 'schedule:':   (context, chain) = ('schedule',   None)

            elif words[0] == 'chain:':
                (context, chain) = ('chain', words[1])
                self.cmdqueue[chain] = queue.Queue()
                self.thread[chain]   = threading.Thread(target=self.chain_thread, args=(chain, self.cmdqueue[chain], self.eventqueue,))

            elif context == 'variables':
                name = words.pop(0)
                self.variables.define(name, words)

            elif context == 'interrupts':
                id = words.pop(0)
                if not id in self.interrupts: self.interrupts[id] = []
                self.interrupts[id].append(Event(words))

            elif context == 'schedule':
                self.cmdqueue['_scheduler'].put({ 'action': 'add', 'data': ScheduleEvent(words) })

            elif context == 'chain':
                self.cmdqueue[chain].put({ 'action': 'add', 'data': ChainEvent(words) })



    def run(self):
        print('main: run')
        self.mainthread.start()



    def event_run(self, event):
        ''' Quit '''
        if event.cmd == 'quit':
            print('{}'.format(event.cmd))
            self.eventqueue.queue.clear()

            for chain in self.cmdqueue:
                print('Quitting', chain)
                self.cmdqueue[chain].queue.clear()

                self.cmdqueue[chain].put({ 'action': 'quit' })
                self.thread[chain].join()

            self.hardware.reset()
            return True

        ''' Chain commands '''
        if event.cmd in ['start', 'stop', 'reset']:
            print('{} {}'.format(event.cmd, event.target))
            self.cmdqueue[event.target].put({ 'action': event.cmd })

        ''' Output commands '''
        if event.cmd in ['on', 'off', 'toggle', 'random']:
            self.hardware.write(event.target, event.cmd)

        ''' Variable commands '''
        if event.cmd == 'set': self.variables.set(event.target, event.params)
        if event.cmd == 'add': self.variables.add(event.target, event.params)
        if event.cmd == 'sub': self.variables.sub(event.target, event.params)
        if event.cmd == 'inc': self.variables.inc(event.target)
        if event.cmd == 'dec': self.variables.dec(event.target)

        if event.cmd == 'read':
            value = self.hardware.read(event.params)
            self.variables.set(event.target, value)
            print ('setting variable {}: {}'.format(event.target, value))

        if event.cmd == 'react':
            events = self.variables.react(event.target)
            for event in events:
                self.eventqueue.put(event)

        return False



    def main_thread(self, eventqueue):
        print('Hello! I\'m main')

        for chain in self.thread:
            self.thread[chain].start()

        quit = False
        while not quit:
            while eventqueue.empty():
                while not self.hardware.interrupt.empty():
                    (type, id) = self.hardware.interrupt.get()

                    if type in self.interrupts and id in self.interrupts[type]:
                        print('INTERRUPT! {} {}'.format(type, id))
                        for event in self.interrupts[type][id]:
                            quit = quit | self.event_run(event)

                sleep(0.01)


            while not eventqueue.empty():
                event = eventqueue.get()
                quit = quit | self.event_run(event)


        print('Bye from main')



    def scheduler_thread(self, cmdqueue, eventqueue):
        print('Hello! I\'m the scheduler')

        events    = []
        counter   = 0
        eventtime = datetime.now()

        quit = False

        while not quit:
            while cmdqueue.empty():
                if len(events) > 0:
                    nowtime = datetime.now()

                    for event in events:
                        if event.test_time(nowtime):
                            eventqueue.put(event)

                sleep(0.1)


            while not cmdqueue.empty():
                cmd = cmdqueue.get()

                if cmd['action'] == 'quit':  quit = True
                if cmd['action'] == 'add':   events.append(cmd['data'])


        events.clear()
        print('Bye from the scheduler')



    def chain_thread(self, name, cmdqueue, eventqueue):
        print('Hello! I\'m {}'.format(name))

        events    = []
        counter   = 0
        eventtime = datetime.now()

        run  = False
        quit = False

        while not quit:
            while cmdqueue.empty():
                if run and len(events) > 0:
                    nowtime = datetime.now()

                    if nowtime > eventtime:
                        eventqueue.put(events[counter])
                        counter = (counter + 1) % len(events)
                        eventtime = nowtime + events[counter].getdelay()

                sleep(0.01)


            while not cmdqueue.empty():
                cmd = cmdqueue.get()

                if cmd['action'] == 'quit':  quit = True
                if cmd['action'] == 'start': run = True
                if cmd['action'] == 'stop':  run = False
                if cmd['action'] == 'reset': counter = 0; eventtime = datetime.now()
                if cmd['action'] == 'add':   events.append(cmd['data'])


        events.clear()
        print('Bye from {}'.format(name))
