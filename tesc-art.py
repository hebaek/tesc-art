#!/usr/bin/env python3

import signal
import time
import pwd

import config

from file     import parse_file, load_config

from hardware import Hardware
from main     import Main



conf     = {}
hardware = None
main     = None
quit     = False



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
    data = parse_file(config.CONFIG_FILE)
    conf = load_config(data)

    signal.signal(signal.SIGHUP,  restart)
    signal.signal(signal.SIGINT,  stop)
    signal.signal(signal.SIGQUIT, stop)
    signal.signal(signal.SIGTERM, stop)

    start()

    while not quit:
        time.sleep(1)

    print ('Quitting...')
