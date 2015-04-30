#!/usr/bin/env python2
import serial
import sys
SERPORT = '/dev/ttyACM0'
SERBAUD = 9600
SERTIMEOUT = 1


def get_pin(pin=12):
    for _ in xrange(10):
        SER = serial.Serial(SERPORT, SERBAUD, timeout=SERTIMEOUT)
        SER.write(str(pin) + " 0\n")
        ret = SER.readline()
        SER.close()
        ret = ret.strip()
        ret = ret.split()
        if len(ret) < 2:
            continue
        if not ret[0].strip() == str(pin):
            continue
        state = ret[1]
        if state.strip() == "0":
            sys.exit(0)
        else:
            print(1)
            sys.exit(1)
    sys.exit(-1)


if __name__ == '__main__':
    get_pin()
