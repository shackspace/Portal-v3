#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from optparse import OptionParser
import serial
import time
import sys
import os
import datetime

KEYMATIC_OPEN_PIN = 1
KEYMATIC_CLOSE_PIN = 2
DOOR_STATE_OUTPUT_PIN = 3
BUZZER_PIN = 4
CLOSEBUTTON_PIN = 10
DOOR_STATE_PIN = 11
DOOR_LOCK_STATE_PIN = 12

LOGFILE = 'portal.log'
LOCKFILE = '/var/run/portal/portal.lock'
STATUSFILE = '/var/run/portal/keyholder'
SERPORT = '/dev/ttyACM0'
SERBAUD = 9600
SERTIMEOUT = 1

LOGLEVEL = 2


def main():
    beep(0.1)
    parser = get_option_parser()
    (options, args) = parser.parse_args()
    check_options(options)
    create_lock(options.name)
    if options.action == 'open':
        msg = 'Door opened by: %s (ID: %s)' % (options.name, options.serial)
        log(msg)
        open_portal()
        if options.nick:
            update_keyholder(options.nick)
        else:
            name = options.name
            name = name.split(' ')
            name[0] = name[0][:3]
            if len(name) > 1:
                name[len(name) - 1] = name[1][:1]
            name = ' '.join(name)
            update_keyholder(name)
    if options.action == 'close':
        msg = 'Door closed by: %s (ID: %s)' % (options.name, options.serial)
        log(msg)
        close_portal()
    remove_lock()


def log(message, level=1):
    if level > LOGLEVEL:
        return
    timestamp = datetime.datetime.now()
    message = str(timestamp) + ':\t' + message + '\n'
    print(message)
    f = open(LOGFILE, 'a')
    f.write(message)
    f.close()


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
    log("set failded for pin %d with state %s" % (pin, state))
    # TODO raise


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
    log("get failded for " + str(pin))


def remove_lock():
    """
    remove the lock file
    """
    try:
        os.remove(LOCKFILE)
    except OSError:
        log("Couldn't remove lock file: %s" % LOCKFILE)


def lockpid_running(pid):
    """
    check if pid is running
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def create_lock(name):
    """
    create a lockfile
    """
    if os.path.isfile(LOCKFILE):
        f = open(LOCKFILE, 'r')
        content = f.read()
        content.strip()
        if lockpid_running(content):
            log('Could not lock open job, locked by %s' % content)
            sys.exit(1)
        else:
            log("Removing lockfile as %s isn't running anymore" % content, 2)
            remove_lock()
    f = open(LOCKFILE, 'w')
    f.write(os.getpid())
    f.close()


def check_options(options):
    if not options.serial:
        print('Please provide a serial')
        sys.exit(1)
    if not options.name:
        print('Please provide a name')
        sys.exit(1)
    if not options.action:
        print('Please specify a aciton (open|close)')
        sys.exit(1)

    valid_actions = ['open', 'close']
    if options.action not in valid_actions:
        print('Option must be open or close')
        sys.exit(1)


def update_keyholder(name):
    """
    update the status file with the current keyholder
    """
    f = open(STATUSFILE, 'w')
    f.write(name)
    f.close()


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
    parser.add_option('--nick',
                      dest='nick',
                      help='OPT: members nickname')
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


def open_keymatic():
    print("opening keymatic")
    set_pin(KEYMATIC_OPEN_PIN, True)
    time.sleep(1)
    set_pin(KEYMATIC_OPEN_PIN, False)


def open_portal():
    """
    Open the door
    """
    for _ in xrange(3):
        open_keymatic()
        time.sleep(5)
        if is_reed_open(15):
            beep_success()
            return
        beep_fail()


def is_reed_open(timeout=0):
    status = get_pin(DOOR_LOCK_STATE_PIN)
    for _ in xrange(timeout):
        status = get_pin(DOOR_LOCK_STATE_PIN)
        log("door lock status: " + str(status), 2)
        if status:
            return True
        time.sleep(1)

    return status


def is_reed_closed(timeout=0):
    status = get_pin(DOOR_LOCK_STATE_PIN)
    for _ in xrange(timeout):
        status = get_pin(DOOR_LOCK_STATE_PIN)
        log("door lock status: " + str(status), 2)
        if not status:
            return True
        time.sleep(1)

    return status


def is_door_button_open():
    return get_pin(DOOR_STATE_PIN)


def close_door():
    log("closing keymatic", 2)
    set_pin(KEYMATIC_CLOSE_PIN, True)
    time.sleep(1)
    set_pin(KEYMATIC_CLOSE_PIN, False)


def close_portal():
    for _ in xrange(30):
        beep(.5)
        if not is_door_button_open():
            log("door closed", 2)
            time.sleep(.5)
            close_door()
            if is_reed_closed(15):
                beep_success()
                return
            else:
                break
        log("door still open", 2)
        time.sleep(0.5)
    alarm()


def alarm():
    log("door close failed")
    beep_alarm()


def beep(duration=0.2):
    set_pin(BUZZER_PIN, True)
    time.sleep(duration)
    set_pin(BUZZER_PIN, False)


def beep_alarm():
    for _ in xrange(30):
        beep(0.1)
        time.sleep(0.1)


def beep_success():
    for _ in xrange(2):
        beep(0.2)
        time.sleep(0.2)


def beep_fail():
    beep(1)

if __name__ == '__main__':
    main()
