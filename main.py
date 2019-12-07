# Public imports
import threading
import queue

from datetime import datetime
from time     import sleep

# Local imports
import config

from event import Event



class Main():
    def __init__(self, hardware):
        print('main: setup')
        self.hardware   = hardware

        self.eventqueue = queue.Queue()
        self.mainthread = threading.Thread(target=self.main_thread, args=(self.eventqueue,))

        self.interrupts = {}
        self.cmdqueue   = {}
        self.thread     = {}



    def clear(self):
        print('main: clear')
        self.eventqueue.queue.clear()

        if self.mainthread.is_alive():
            self.eventqueue.put(Event(['quit']))
            self.mainthread.join()



    def reset(self):
        print('main: reset')

        self.hardware.reset()
        self.eventqueue.queue.clear()

        if self.mainthread.is_alive():
            self.eventqueue.put(Event(['quit']))
            self.mainthread.join()
        
        self.mainthread = threading.Thread(target=self.main_thread, args=(self.eventqueue,))

        self.interrupts = {}
        self.cmdqueue   = {}
        self.thread     = {}



    def load(self, filename):
        print('main: load')

        lines  = []

        try:
            with open(filename) as f:
                filedata = f.read()
                lines = [line for line in filedata.split('\n') if len(line) > 1 and line[0] != '#']

        except Exception:
            print('Can\'t open events file!')
            lines = ['chain: boot', 'quit']


        context = None
        for line in lines:
            words = line.split()
            if words[0] == 'interrupts:':
                (context, chain) = ('interrupts', None)

            elif words[0] == 'chain:':
                (context, chain) = ('chain', words[1])
                self.cmdqueue[chain] = queue.Queue()
                self.thread[chain]   = threading.Thread(target=self.chain_thread, args=(chain, self.cmdqueue[chain], self.eventqueue,))

            elif context == 'interrupts':
                type = words.pop(0)
                id   = words.pop(0)

                if not type in self.interrupts: self.interrupts[type] = {}
                if not id in self.interrupts[type]: self.interrupts[type][id] = []
                self.interrupts[type][id].append(Event(words))

            elif context == 'chain':
                self.cmdqueue[chain].put({ 'action': 'add', 'data': Event(words) })



    def run(self):
        print('main: run')
        self.mainthread.start()



    def interrupt(self, type, id):
        self.hardware.interrupt = (type, id)



    def event_run(self, event):
        ''' Quit '''
        if event.cmd == 'quit':
            print('{}'.format(event.cmd))
            for chain in self.cmdqueue:
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

        ''' Input commands '''
        if event.cmd == 'read':
            pass

        return False



    def main_thread(self, eventqueue):
        print('Hello! I\'m main')

        for chain in self.thread:
            self.thread[chain].start()

        self.cmdqueue['boot'].put({ 'action': 'start' })


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

        print('Bye from {}'.format(name))
