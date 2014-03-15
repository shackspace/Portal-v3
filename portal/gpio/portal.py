#!/usr/bin/env python2
#-*- coding:utf-8 -*-

from optparse import OptionParser
try:
    import RPi.GPIO as GPIO
    local = False
except RuntimeError, e:
    print("Running in local mode")
    local = True
import time
import sys
import os
import datetime

OPENPIN = 17
CLOSEPIN = 18
DOOR = 24
LOGFILE = 'portal.log'
LOCKFILE = '/tmp/portal.lock'

def main():
    if not local:
        setup()
    parser = get_option_parser()
    (options, args) = parser.parse_args()
    check_options(options)
    create_lock(options.name)
    if options.action == 'open':
        msg = 'Door opened by: %s (ID: %s)' % (options.name, options.serial)
        log(msg)
        open_portal(local)
    if options.action == 'close':
        msg = 'Door closed by: %s (ID: %s)' % (options.name, options.serial)
        log(msg)
        close_portal(local)
    remove_lock()

def log(message):
    timestamp = datetime.datetime.now()
    message = str(timestamp) + ':\t' + message + '\n'
    f = open(LOGFILE, 'a')
    f.write(message)
    f.close()
    

def remove_lock():
    try:
        os.remove(LOCKFILE)
    except OSError, e:
        log("Couldn't remove lock file: %s" % LOCKFILE)
    
def create_lock(name):
    """
    create a lockfile
    """
    if os.path.isfile(LOCKFILE):
        f = open(LOCKFILE, 'r')
        content = f.read()
        content.strip()
        log('Could not lock open job, locked by %s' % content)
        sys.exit(1)
    else:
        f = open(LOCKFILE, 'w')
        f.write(name)
        f.close()


def check_options(options):
    if not options.serial:
        print('Please provide a serial')
        sys.exit(1)
    if not options.name:
        print('Please provide a name')
        sys.exit(1)
    if not options.action:
        print('Please specify a aciton (open|close)')
        sys.exit(1)

    valid_actions = ['open', 'close']
    if not options.action in valid_actions: 
        print('Option must be open or close')
        sys.exit(1)


def get_option_parser():
    """
    create OptionParser obejct and add options
    """
    parser = OptionParser()
    parser.add_option('-s', '--serial',
                      dest='serial',
                      help='members ID')
    parser.add_option('-n', '--name',
                      dest='name',
                      help='keymembers name name_surname')
    parser.add_option('-a', '--action',
                      dest='action',
                      help='open|close')
    parser.add_option('-l', '--last',
                      dest='last',
                      help='OPT: last valid day of the key')
    parser.add_option('-f', '--first',
                      dest='first',
                      help='OPT: first valid day of the key')
    return parser

def setup():        
    """
    initialize GPIOs with their functions
    """
    #define board layout
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #define OPENPIN as output
    GPIO.setup(OPENPIN, GPIO.OUT)
    #define CLOSEPIN as output
    GPIO.setup(CLOSEPIN, GPIO.OUT)
    #define doorpin as input which is active high
    GPIO.setup(DOOR, GPIO.IN, GPIO.PUD_DOWN)

def open_portal(local):
    """
    Open the door
    """
    if not local:
        GPIO.output(OPENPIN, False)
        time.sleep(1)
        GPIO.output(OPENPIN, True)
    else:
        print('Opened door')

def close_portal(local):
    """
    close the door
    """
    #only close the door if it is physically closed
    if not local:
        if GPIO.input(DOOR) == 1:
            GPIO.output(CLOSEPIN, False)
            time.sleep(1)
            GPIO.output(CLOSEPIN, True)
        else:
            close_failed()
    else:
        print('Closed door')

def close_failed():
    """
    inform user that close was unsuccessfull
    """
    log('close failed!') 
    #TODO: Play a sound to notify of failure


if __name__ == '__main__':
    main()
