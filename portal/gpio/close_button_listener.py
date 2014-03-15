#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import subprocess

CLOSEBUTTON = 24

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CLOSEBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(CLOSEBUTTON, GPIO.RISING)
    while True:
        if GPIO.event_detected(CLOSEBUTTON):
            GPIO.remove_event_detect(CLOSEBUTTON)
            close_door()
            GPIO.add_event_detect(CLOSEBUTTON, GPIO.RISING)

    
def close_door():
    try:
        subprocess.Popen('./portal.py -s 0 -n button -a close')
    except subprocess.CalledProcessError, e:
        #TODO: Play a error sound!
        print("Couldn't execute close command")
    print('Closing door')
    time.sleep(10)
    

if __name__ == '__main__':
    GPIO.wait_for_interrupts()
    main()
