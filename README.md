# tesc-art
Timed Event Send/Control for art

This tool lets you control the GPIO of a Raspberry Pi using simple lists of timed events.

## Getting started

### What you need
* A Raspberry Pi
* Python 3

### Installing
* Download a copy of tesc-art using `git clone https://github.com/hebaek/tesc-art`
* Install GPIO using `sudo apt install python3-rpi-lgpio`
* In the tesc-art directory, run `sudo make install user=$(whoami) home=~`
* Copy the example files and start scripting!

* To run automatically at boot, do the following:
- run `crontab -e`
- add the line `@reboot /usr/bin/tesc-art start`


## The files you need to worry about

### tesc-art.conf
This contains the file names of your chosen hardware setup and events files.

### hwsetup.txt
This file is a mapping between GPIO pins and target names.
The section headers in this file defines if the pin is an interrupt, an input or an output.

### events.txt
This file is the bread and butter of your application. It has four types of lists:
* variables
* interrupts
* schedule
* chains

#### variables
In the variables section, you define variables and how to react to their values.
A list of comparators is included in the example file.
If the variable matches the comparator, the event will fire.
You trigger a reaction with the command `react`.

#### interrupts
In the interrupts section, you define events to be fired from interrupts. This should probably be to start or stop a chain.

#### schedule
In the schedule section, you define events which will trigger at specific times on specific dates or weekdays.
The timespec is written in `hh:mm:ss`-format, and optionally a `weekday` or a `date`. Se the example file for details about formats.
It you omit a part of the date or time, it will trigger every time the rest of the timespec matches.
A special schedule type `boot` triggers at lauch.

#### chains
A chain is a looping list of timed events. It contains a delay consisting of a fixed and a random part, a command and a target.
The target are the ones defined in `hwsetup.txt`, and the command is one of the following:
```
quit

start  <chain>
stop   <chain>
reset  <chain>

on     <target>
off    <target>
toggle <target>
random <target>

set    <variable> <value|variable>
read   <variable> <input>
react  <variable>

add    <variable> <value|variable>
sub    <variable> <value|variable>
inc    <variable>
dec    <variable>
```


## Licence
tesc-art uses the GPLv2 licence.
