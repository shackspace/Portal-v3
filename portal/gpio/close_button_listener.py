#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import RPi.GPIO as GPIO

CLOSEBUTTON = 24

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CLOSEBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_callback(CLOSEBUTTON, GPIO.RISING, callback=close_door, bouncetime=20)
    GPIO.wait_for_interrupts()

def close_door():
    print('Closing door')
    

if __name__ == '__main__':
    main()
