#!/usr/bin/env python2
import sys
from portal import SerialCommunication, DOOR_LOCK_STATE_PIN


if __name__ == '__main__':
    with SerialCommunication() as serialcommunication:
        state = serialcommunication.get_pin(DOOR_LOCK_STATE_PIN)
    if state is True:
        sys.exit(1)
    if state is False:
        sys.exit(0)
    sys.exit(-1)
