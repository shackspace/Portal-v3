#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

OPENPIN = 17
CLOSEPIN = 18
DOOR = 24

def main():
    setup()
    open()
    close()

def setup():        
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(OPENPIN, GPIO.OUT)
    GPIO.setup(CLOSEPIN, GPIO.OUT)
    GPIO.setup(DOOR, GPIO.IN, GPIO.PUD_DOWN)

def open():
    GPIO.output(OPENPIN, False)
    time.sleep(1)
    GPIO.output(OPENPIN, True)

def close():
    if GPIO.input(DOOR) == 1:
        GPIO.output(CLOSEPIN, False)
        time.sleep(1)
        GPIO.output(CLOSEPIN, True)
    else:
        close_failed()

def close_failed():
    print("you're made of stupid")
    #TODO: Play a sound to notify of failure


if __name__ == '__main__':
    main()
