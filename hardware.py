# Public imports
import queue

from random import randrange

# Local imports
import config

# Try to import GPIO. If it succeeds, we are probably on a real Raspberry PI
try:
    import RPi.GPIO as GPIO
    config.REAL_PI = True

except ImportError:
    print ('No pi...')



class Hardware():
    def __init__(self, filename):
        print('hardware: setup')

        self.interrupt = queue.Queue()
        self.targets   = {}
        self.buffer    = {}

        self.load(filename)

        if config.REAL_PI:
            GPIO.setmode(GPIO.BCM)

            for pin in [self.targets[x]['pin'] for x in self.targets if self.targets[x]['type'] == 'output']:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, 0)

            for pin in [self.targets[x]['pin'] for x in self.targets if self.targets[x]['type'] == 'input']:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

            for pin in [self.targets[x]['pin'] for x in self.targets if self.targets[x]['type'] == 'interrupt']:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.add_event_detect(pin, GPIO.RISING, callback=self.interrupt_handler, bouncetime=1000)

        self.reset()



    def load(self, filename):
        lines = []

        try:
            with open(filename) as f:
                filedata = f.read()
                lines = [line for line in filedata.split('\n') if len(line) > 1 and line[0] != '#']

        except Exception:
            print('Can\'t open setup file!')

        context = None
        for line in lines:
            words = line.split()

            if   line == 'interrupts:': context = 'interrupts'
            elif line == 'inputs:':     context = 'inputs'
            elif line == 'outputs:':    context = 'outputs'

            elif context == 'interrupts': self.targets[words[1]] = { 'pin': int(words[0]), 'type': 'interrupt' }
            elif context == 'inputs':     self.targets[words[1]] = { 'pin': int(words[0]), 'type': 'input'     }
            elif context == 'outputs':    self.targets[words[1]] = { 'pin': int(words[0]), 'type': 'output'    }



    def clear(self):
        print('hardware: clear')
        if config.REAL_PI:
            GPIO.cleanup()



    def reset(self):
        for target in self.targets:
            self.buffer[target] = 0

        if config.REAL_PI:
            for pin in [self.targets[x]['pin'] for x in self.targets if self.targets[x]['type'] == 'output']:
                GPIO.output(pin, 0)



    def interrupt_handler(self, pin):
        for target in [x for x in self.targets if self.targets[x]['type'] == 'interrupt' and self.targets[x]['pin'] == pin]:
            print('hardware: interrupt_handler - {}'.format(target))
            self.interrupt.put(('GPIO', '{}'.format(target)))



    def read(self, input):
        if config.REAL_PI:
            self.buffer[input] = GPIO.input(self.targets[input]['pin'])

        print ('reading pin {:>2}: [{:6}]'.format(self.targets[input]['pin'], self.buffer[input]))
        return self.buffer[input]



    def write(self, target, cmd):
        print ('writing pin {:>2}: [{:6}] - {}'.format(self.targets[target]['pin'], cmd, target))
        if cmd == 'on':     self.buffer[target] |= 1
        if cmd == 'off':    self.buffer[target] &= 0
        if cmd == 'toggle': self.buffer[target]  = (self.buffer[target] + 1) % 2
        if cmd == 'random': self.buffer[target]  = randrange(0, 2)

        if config.REAL_PI:
            GPIO.output(self.targets[target]['pin'], self.buffer[target])
