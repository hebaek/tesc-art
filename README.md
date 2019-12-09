# tesc-art
Timed Event Send/Control - Art
This tool lets you control the GPIO of a Raspberry Pi using simple lists of timed events.

## Getting started

### Prerequisites
* You need a Raspberry Pi
* You need Python 3

### Installing
* Download a copy of tesc-art using `git clone https://github.com/hebaek/tesc-art`
* In the tesc-art directory, run `make install`.
* Copy the example files and start scripting!

* To run tesc-art on startup, add the following to rc.local (before `exit 0`:
```
/usr/local/src/tesc-art.py > <your favorite logfile> &
```

## The files you need to worry about

### tesc-art.conf
This contains the file names of your chosen setup and events-files.

### setup.txt
This file is a mapping between GPIO pins and target names.
The section header in this file defines if the pin is an interrupt, an input (not implemented) or an output.

### events.txt
This file is the bread and butter of your application. It has two types of lists:
* interrupts
* chains

In the interrupts section, you define events to be fired from interrupts. This should probably be to start or stop a chain.

A chain is a looping list of timed events. It contains a delay, a random amount of time to be randomly added to the delay, a command and a target.
The targets are the ones defined in `setup.txt`, and the commands is one of the following:
```
quit

start  <chain>
stop   <chain>
reset  <chain>

on     <target>
off    <target>
toggle <target>
random <target>
```

The specian chain `boot` is the only one started automaticlly, you should probably only use this to start the _real_ chains.