#!/usr/bin/env python3

import signal
import time
import pwd

import config

from hardware import Hardware
from main     import Main



conf     = {}
hardware = None
main     = None
quit     = False



def load_config():
    print ('Loading config...')

    with open(config.CONFIG_FILE) as f:
        filedata = f.read()
        lines = [line for line in filedata.split('\n') if len(line) > 0 and line[0] != '#']

        for line in lines:
            words = line.split()
            conf[words[0]] = words[1]

    return conf



def start():
    print ('Starting...')

    global hardware, main
    hardware = Hardware(conf['setup'])
    main     = Main(hardware)

    main.reset()
    main.load(conf['events'])
    main.run()



def restart(signum, frame):
    print ('Restarting... (signal {})'.format(signum))
    stop(signum, frame)
    load_config()
    start()



def stop(signum, frame):
    print ('Stopping... (signal {})'.format(signum))

    global main, hardware
    main.clear()
    hardware.clear()

    if signum != signal.SIGHUP:
        global quit
        quit = True



def reload(signum, frame):
    print ('Reloading... (signal {})'.format(signum))

    main.reset()
    main.load(conf['events'])
    main.run()



if __name__ == '__main__':
    load_config()

    signal.signal(signal.SIGHUP,  restart)
    signal.signal(signal.SIGINT,  stop)
    signal.signal(signal.SIGQUIT, stop)
    signal.signal(signal.SIGTERM, stop)

    start()

    while not quit:
        time.sleep(1)

    print ('Quitting...')
