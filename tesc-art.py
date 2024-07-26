#!/usr/bin/env python3

import logging
import signal
import time
import pwd

import config

from file     import parse_file, load_config, load_events

from hardware import Hardware
from main     import Main



conf     = {}
logger   = logging.getLogger(__name__)
hardware = None
main     = None
quit     = False



def start():
    logger.info('Starting...')

    global hardware, main
    hardware = Hardware(conf['hwsetup'])
    main     = Main(hardware)

    main.reset()
    main.load(conf['events'])
    main.run()



def restart(signum, frame):
    logger.info('Restarting... (signal {})'.format(signum))
    stop(signum, frame)
    load_config()
    start()



def stop(signum, frame):
    logger.info('Stopping... (signal {})'.format(signum))

    global main, hardware
    main.clear()
    hardware.clear()

    if signum != signal.SIGHUP:
        global quit
        quit = True



def reload(signum, frame):
    logger.info('Reloading... (signal {})'.format(signum))

    main.reset()
    main.load(conf['events'])
    main.run()



if __name__ == '__main__':
    data = parse_file(config.CONFIG_FILE)
    conf = load_config(data)

    logging.basicConfig(filename=conf['logfile'], filemode='w', level=logging.INFO)

    signal.signal(signal.SIGHUP,  restart)
    signal.signal(signal.SIGINT,  stop)
    signal.signal(signal.SIGQUIT, stop)
    signal.signal(signal.SIGTERM, stop)

    start()

    while not quit:
        time.sleep(1)

    logger.info('Quitting...')
