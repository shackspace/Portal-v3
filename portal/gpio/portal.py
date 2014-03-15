#!/usr/bin/env python2
#-*- coding:utf-8 -*-

from optparse import OptionParser
try:
    import RPi.GPIO as GPIO
except RuntimeError, e:
    print("Running in local mode")
    local = True
import time

OPENPIN = 17
CLOSEPIN = 18
DOOR = 24

def main():
    if not local:
        setup()
    parser = get_option_parser()
    (options, args) = parser.parse_args()
    open(local)
    

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

def open(local):
    """
    Open the door
    """
    if not local:
        GPIO.output(OPENPIN, False)
        time.sleep(1)
        GPIO.output(OPENPIN, True)
    else:
        print('Opened door')

def close(local):
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
    print("you're made of stupid")
    #TODO: Play a sound to notify of failure


if __name__ == '__main__':
    main()
