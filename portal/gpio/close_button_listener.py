#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import subprocess
import time

CLOSEBUTTON = 24
PORTALSCRIPTPATH = '/root/portalv3/software/portal/gpio/'

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
    cmd = PORTALSCRIPTPATH + 'portal.py -s 0 -n button -a close'
    try:
        subprocess.call(cmd.split())
    except subprocess.CalledProcessError, e:
        #TODO: Play a error sound!
        print("Couldn't execute close command")
    print('Closing door')
    time.sleep(10)
    

if __name__ == '__main__':
    main()
