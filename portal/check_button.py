#!/usr/bin/env python2
import serial
import subprocess

SERPORT = '/dev/ttyACM0'
SERBAUD = 9600
SERTIMEOUT = 1

BUTTON_PIN = 20


def set_pin(pin, state):
    if state:
        state = "1"
    else:
        state = "0"
    # print ("set", pin, state)

    for _ in xrange(10):
        SER = serial.Serial(SERPORT, SERBAUD, timeout=SERTIMEOUT)
        SER.write(str(pin) + " " + state + "\n")
        ret = SER.readline()
        SER.close()

        # org = ret
        ret = ret.strip()
        ret = ret.split()
        if len(ret) < 2:
            # print ("fail: set to short", pin, state, org )
            continue
        if not ret[0].strip() == str(pin):
            # print ("fail: set", pin, state, org)
            continue
        set_state = ret[1]
        if set_state.strip() == state:
            # print ("set", pin, state, org)
            return
        else:
            # print ("fail: set", pin, state, org)
            continue


def get_pin(pin):
    for _ in xrange(10):
        SER = serial.Serial(SERPORT, SERBAUD, timeout=SERTIMEOUT)
        SER.write(str(pin) + " 0\n")
        ret = SER.readline()
        SER.close()
        # org = ret
        ret = ret.strip()
        ret = ret.split()
        if len(ret) < 2:
            # print ("fail: get to short", pin, org )
            continue
        if not ret[0].strip() == str(pin):
            # print ("fail: get", pin, org)
            continue
        state = ret[1]
        if state.strip() == "0":
            # print ("get", pin, org, state, False)
            return False
        else:
            # print ("get", pin, org, state, True)
            return True


def main():
    button_pushed = get_pin(BUTTON_PIN)
    if button_pushed:
        print "door close requested by button"
        subprocess.call("/opt/Portal-v3/portal/portal.py",
                        ["-a", "close",
                         "-s", "0000",
                         "-n", "\"CloseButton\"",
                         "-l", "2023-04-02",
                         "-f", "2015-04-25",
                         "--nick", "\"CloseButton\""])

        set_pin(BUTTON_PIN, True)


if __name__ == '__main__':
    main()
