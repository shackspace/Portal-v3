#!/usr/bin/env python2
import serial
import subprocess
import time
import datetime

SERPORT = '/dev/ttyACM0'
SERBAUD = 9600
SERTIMEOUT = 1

BUTTON_PIN = 20

from portal import SerialCommunication


def main():
    with SerialCommunication() as serialcommunication:
        button_pushed = serialcommunication.get_pin(BUTTON_PIN)
    if button_pushed:
        print str(datetime.datetime.now()) + ": door close requested by button"
        subprocess.call(["/opt/Portal-v3/portal/portal.py",
                         "-a", "close",
                         "-s", "0000",
                         "-n", "\"CloseButton\"",
                         "-l", "2023-04-02",
                         "-f", "2015-04-25",
                         "--nick", "\"CloseButton\""])
        with SerialCommunication() as serialcommunication:
            serialcommunication.set_pin(BUTTON_PIN, True, expected="0")


if __name__ == '__main__':
    while True:
        main()
        time.sleep(1)
