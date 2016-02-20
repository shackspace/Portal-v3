#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from optparse import OptionParser
import serial
import time
import sys
import os
import grp
import pwd
import datetime

KEYMATIC_OPEN_PIN = 1
KEYMATIC_CLOSE_PIN = 2
DOOR_STATE_OUTPUT_PIN = 3
BUZZER_PIN = 4
CLOSEBUTTON_PIN = 10
DOOR_STATE_PIN = 11
DOOR_LOCK_STATE_PIN = 12

LOGFILE = '/var/log/portal/portal.log'
LOCKFILE = '/var/run/lock/portal.lock'
STATUSFILE = '/var/log/portal/keyholder'
SERPORT = '/dev/ttyACM0'
SERBAUD = 9600
SERTIMEOUT = 1

LOGLEVEL = 2


class SerialCommunication():
    def __init__(self, serial_port=SERPORT, serial_baud=SERBAUD, serial_timeout=SERTIMEOUT):
        self.serial_port = serial_port
        self.serial_baud = serial_baud
        self.serial_timeout = serial_timeout
        self.ser = serial.Serial(self.serial_port, self.serial_baud, timeout=self.serial_timeout)

    def __enter__(self):
        # self.ser = serial.Serial(self.serial_port, self.serial_baud, timeout=self.serial_timeout)
        return self

    def __exit__(self, type, value, traceback):
        self.ser.close()

    def validate_connection(self):
        if self.ser.closed:
            self.ser = serial.Serial(self.serial_port, self.serial_baud, timeout=self.serial_timeout)

    def get_pin(self, pin):
        self.validate_connection()
        for _ in xrange(10):
            self.ser.write(str(pin) + " 0\n")
            ret = self.ser.readline()
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

    def set_pin(self, pin, state, expected=None):
        self.validate_connection()
        if state:
            state = "1"
        else:
            state = "0"
        # print ("set", pin, state)

        if expected is None:
            expected = state

        for _ in xrange(10):
            self.ser.write(str(pin) + " " + state + "\n")
            ret = self.ser.readline()

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
            if set_state.strip() == expected:
                # print ("set", pin, state, org)
                return
            else:
                # print ("fail: set", pin, state, org)
                continue
        log("set failded for pin %d with state %s" % (pin, state))
        # TODO raise


class Portal():
    def __init__(self, serial_port=SERPORT, serial_baud=SERBAUD, serial_timeout=SERTIMEOUT):
        self.serial = SerialCommunication(serial_port=SERPORT, serial_baud=SERBAUD, serial_timeout=SERTIMEOUT)

    def __enter__(self):
        self.serial.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.serial.__exit__(type, value, traceback)

    def open_portal(self):
        """
        Open the door
        """
        for _ in xrange(3):
            print("opening keymatic")
            self.serial.set_pin(KEYMATIC_OPEN_PIN, True)
            time.sleep(1)
            self.serial.set_pin(KEYMATIC_OPEN_PIN, False)
            time.sleep(5)
            if self.is_reed_open(15):
                self.beep_success()
                return
            self.beep_fail()

    def is_reed_open(self, timeout=0):
        status = self.serial.get_pin(DOOR_LOCK_STATE_PIN)
        for _ in xrange(timeout):
            status = self.serial.get_pin(DOOR_LOCK_STATE_PIN)
            log("door lock status: " + str(status), 2)
            if status:
                return True
            time.sleep(1)
        return status

    def is_reed_closed(self, timeout=0):
        status = self.serial.get_pin(DOOR_LOCK_STATE_PIN)
        for _ in xrange(timeout):
            status = self.serial.get_pin(DOOR_LOCK_STATE_PIN)
            log("door lock status: " + str(status), 2)
            if not status:
                return True
            time.sleep(1)

        return not status

    def is_door_button_open(self):
        return self.serial.get_pin(DOOR_STATE_PIN)

    def close_door(self):
        log("closing keymatic", 2)
        self.serial.set_pin(KEYMATIC_CLOSE_PIN, True)
        time.sleep(1)
        self.serial.set_pin(KEYMATIC_CLOSE_PIN, False)

    def close_portal(self):
        for _ in xrange(30):
            self.beep(.5)
            if not self.is_door_button_open():
                log("door closed", 2)
                time.sleep(.5)
                self.serial.set_pin(KEYMATIC_CLOSE_PIN, True)
                time.sleep(1)
                self.serial.set_pin(KEYMATIC_CLOSE_PIN, False)
                if self.is_reed_closed(15):
                    self.beep_success()
                    return
                else:
                    break
            log("door still open", 2)
            time.sleep(0.5)
        self.alarm()

    def alarm(self):
        log("door close failed")
        self.beep_alarm()

    def beep(self, duration=0.2):
        self.serial.set_pin(BUZZER_PIN, True)
        time.sleep(duration)
        self.serial.set_pin(BUZZER_PIN, False)

    def beep_alarm(self):
        for _ in xrange(30):
            self.beep(0.1)
            time.sleep(0.1)

    def beep_success(self):
        for _ in xrange(2):
            self.beep(0.2)
            time.sleep(0.2)

    def beep_fail(self):
        self.beep(1)


class Lockfile():
    def __init__(self, lockfile):
        self.lockfile = lockfile
        self.create_lock()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.remove_lock()

    def create_lock(self):
        """
        create a lockfile
        """
        if os.path.isfile(LOCKFILE):
            f = open(self.lockfile, 'r')
            content = f.read()
            content.strip()
            if self.lockpid_running(content):
                log('Could not lock open job, locked by %s' % content)
                sys.exit(1)
            else:
                log("Removing lockfile as %s isn't running anymore" % content, 2)
                self.remove_lock()
        with open(self.lockfile, 'w') as f:
            f.write(str(os.getpid()))

    def remove_lock(self):
        """
        remove the lock file
        """
        try:
            os.remove(self.lockfile)
        except OSError:
            log("Couldn't remove lock file: %s" % self.lockfile)

    def lockpid_running(self, pid):
        """
        check if pid is running
        """
        try:
            os.kill(int(pid), 0)
        except OSError:
            return False
        else:
            return True


def main():
    motd()
    parser = get_option_parser()
    (options, args) = parser.parse_args()
    check_options(options)
    with Lockfile(LOCKFILE):
        with Portal() as portal:
            portal.beep(0.1)
            if options.action == 'open':
                msg = 'Door opened by: %s (ID: %s)' % (options.name, options.serial)
                log(msg)
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
                portal.open_portal()
            if options.action == 'close':
                msg = 'Door closed by: %s (ID: %s)' % (options.name, options.serial)
                log(msg)
                portal.close_portal()


def motd():
    with open('/opt/Portal-v3/portal/motd.txt', 'r') as f:
        for line in f.readlines():
            print line,


def log(message, level=1):
    if level > LOGLEVEL:
        return
    timestamp = datetime.datetime.now()
    message = str(timestamp) + ':\t' + message
    print(message)
    f = open(LOGFILE, 'a')
    f.write(message + "\n")
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
    with open(STATUSFILE, 'w') as f:
        f.write(name)
        gid = grp.getgrnam("portal").gr_gid
        uid = uid = pwd.getpwnam("open").pw_uid
        os.chown(STATUSFILE, uid, gid)


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


if __name__ == '__main__':
    main()
