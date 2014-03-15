#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import RPi.GPIO as GPIO

CLOSEBUTTON = 24

def main():
    GPIO.add_event_callback(CLOSEBUTTON, callback=close_door, pull_up_down=RPIO.PUD_DOWN)
    GPIO.wait_for_interrupts()

def close_door():
    print('Closing door')
    

if __name__ == '__main__':
    main()
