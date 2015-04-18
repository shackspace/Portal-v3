#!/usr/env python3
#!/opt/Portal-v3/portal/gpio/env/bin/python
# -*- coding:utf-8 -*-

from optparse import OptionParser
import serial
import time
import sys
import os
import datetime

KEYMATIC_OPEN_PING = 1
KEYMATIC_CLOSE_PING = 2
DOOR_STATE_PIN = 3
BUZZER_PIN = 4
CLOSEBUTTON_PIN = 10
DOOR_STATE_OUTPUT_PIN = 11
DOOR_LOCK_STATE_PIN = 12

LOGFILE = 'portal.log'
LOCKFILE = '/tmp/portal.lock'
STATUSFILE = '/tmp/keyholder'

SER = serial.Serial(0)


def main():
    parser = get_option_parser()
    (options, args) = parser.parse_args()
    check_options(options)
    create_lock(options.name)
    if options.action == 'open':
        msg = 'Door opened by: %s (ID: %s)' % (options.name, options.serial)
        log(msg)
        open_portal()
    if options.action == 'close':
        msg = 'Door closed by: %s (ID: %s)' % (options.name, options.serial)
        log(msg)
        close_portal()
    remove_lock()

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


def log(message):
    timestamp = datetime.datetime.now()
    message = str(timestamp) + ':\t' + message + '\n'
    f = open(LOGFILE, 'a')
    f.write(message)
    f.close()


def set_pin(pin, state):
    if state:
        state = "1"
    else:
        state = "0"
    SER.write(str(pin) + " " + state + "\n")


def get_pin(pin):
    SER.write(str(pin) + " 0\n")
    state = SER.readline()
    if state.strip() == 0:
        return False
    else:
        return True


def remove_lock():
    """
    remove the lock file
    """
    try:
        os.remove(LOCKFILE)
    except OSError:
        log("Couldn't remove lock file: %s" % LOCKFILE)


def create_lock(name):
    """
    create a lockfile
    """
    if os.path.isfile(LOCKFILE):
        f = open(LOCKFILE, 'r')
        content = f.read()
        content.strip()
        log('Could not lock open job, locked by %s' % content)
        sys.exit(1)
    else:
        f = open(LOCKFILE, 'w')
        f.write(name)
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


def open_portal():
    """
    Open the door
    """
    set_pin(KEYMATIC_OPEN_PING, True)
    time.sleep(1)
    set_pin(KEYMATIC_OPEN_PING, False)


def close_portal(local):
    """
    close the door
    """
    # only close the door if it is physically closed
    for second in xrange(30):
        if second % 2 == 0:
            set_pin(BUZZER_PIN, True)
        else:
            set_pin(BUZZER_PIN, False)
        time.sleep(1)
        if get_pin(DOOR_STATE_PIN):
            for smallsec in xrange(10):
                if smallsec % 2 == 0:
                    set_pin(BUZZER_PIN, True)
                else:
                    set_pin(BUZZER_PIN, False)
                time.sleep(0.2)
            set_pin(BUZZER_PIN, False)
            if not get_pin(DOOR_STATE_PIN):
                continue
            set_pin(KEYMATIC_CLOSE_PING, True)
            time.sleep(1)
            set_pin(KEYMATIC_CLOSE_PING, False)
            # TODO test door close status
            break
    else:  # executes if for loop is not left by break
        close_timeout()


def close_timeout():
    """
    inform user of timeout
    """
    log('close timeout!')
    for smallsec in xrange(8):
        if smallsec % 2 == 0:
            set_pin(BUZZER_PIN, True)
        else:
            set_pin(BUZZER_PIN, False)
        time.sleep(0.2)


if __name__ == '__main__':
    main()
