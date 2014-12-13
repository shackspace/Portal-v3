#!/opt/Portal-v3/portal/gpio/env/bin/python
# -*- coding:utf-8 -*-

from optparse import OptionParser
try:
    import RPi.GPIO as GPIO
    local = False
except RuntimeError, e:
    print("Running in local mode")
    local = True
import time
import sys
import os
import datetime

OPENPIN = 17
CLOSEPIN = 18
DOORPIN = 24
BUZZERPIN = 22

LOGFILE = 'portal.log'
LOCKFILE = '/tmp/portal.lock'
STATUSFILE = '/tmp/keyholder'


def main():
    if not local:
        setup()
    parser = get_option_parser()
    (options, args) = parser.parse_args()
    check_options(options)
    create_lock(options.name)
    if options.action == 'open':
        msg = 'Door opened by: %s (ID: %s)' % (options.name, options.serial)
        log(msg)
        open_portal(local)
    if options.action == 'close':
        msg = 'Door closed by: %s (ID: %s)' % (options.name, options.serial)
        log(msg)
        close_portal(local)
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


def setup():
    """
    initialize GPIOs with their functions
    """
    # define board layout
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # define OPENPIN as output
    GPIO.setup(OPENPIN, GPIO.OUT)
    # define CLOSEPIN as output
    GPIO.setup(CLOSEPIN, GPIO.OUT)
    # define BUZZERPIN as output
    GPIO.setup(BUZZERPIN, GPIO.OUT)
    # define doorpin as input which is active high
    GPIO.setup(DOORPIN, GPIO.IN, GPIO.PUD_DOWN)


def open_portal(local):
    """
    Open the door
    """
    if not local:
        GPIO.output(OPENPIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(OPENPIN, GPIO.LOW)
    else:
        print('Opened door')


def close_portal(local):
    """
    close the door
    """
    # only close the door if it is physically closed
    if not local:
        for second in xrange(30):
            if second % 2 == 0:
                GPIO.output(BUZZERPIN, GPIO.HIGH)
            else:
                GPIO.output(BUZZERPIN, GPIO.LOW)
                pass
            time.sleep(1)
            if GPIO.input(DOORPIN) == GPIO.HIGH:
                for smallsec in xrange(10):
                    if smallsec % 2 == 0:
                        GPIO.output(BUZZERPIN, GPIO.HIGH)
                    else:
                        GPIO.output(BUZZERPIN, GPIO.LOW)
                    time.sleep(0.2)
                GPIO.output(BUZZERPIN, GPIO.LOW)
                if GPIO.input(DOORPIN) == GPIO.LOW:
                    continue
                GPIO.output(CLOSEPIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(CLOSEPIN, GPIO.LOW)
                # TODO test door close status
                break
        else:  # executes if for loop is not left by break
            close_timeout()
    else:
        print('Closed door')


def close_timeout():
    """
    inform user of timeout
    """
    log('close timeout!')
    for smallsec in xrange(8):
        if smallsec % 2 == 0:
            GPIO.output(BUZZERPIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZERPIN, GPIO.LOW)
        time.sleep(0.2)


if __name__ == '__main__':
    main()
