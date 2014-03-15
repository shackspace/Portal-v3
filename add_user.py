#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import sqlite3
import sys
from optparse import OptionParser


DATABASE = 'shackspacekey.sqlite'


def main():
    parser = OptionParser()
    parser.add_option('-k',
                      dest='keyfile',
                      help='keyfile')
    parser.add_option('-s',
                      dest='serial',
                      help='membership number')
    parser.add_option('-n',
                      dest='name',
                      help='member\'s name')
    parser.add_option('-l',
                      dest='surname',
                      help='member\'s surname')
    parser.add_option('--nick',
                      dest='nick',
                      help='OPTIONAL: member\'s nickname')
    parser.add_option('--first-valid',
                      dest='first',
                      help='OPTIONAL: time at which key\'s validity begins' +
                      '(YYYYMMDD)')
    parser.add_option('--last-valid',
                      dest='last',
                      help='OPTIONAL: time at which key\' validity ends' +
                      '(YYYYMMDD)')

    (options, args) = parser.parse_args()
    (cur, conn) = get_db()

    if not options.serial:
        print('Please provide a membership number')
        sys.exit(1)

    if not options.keyfile:
        print('Please provide a keyfile')
        sys.exit(1)

    if not options.name:
        print('Please provide a name')
        sys.exit(1)

    if not options.surname:
        print('Please provide a surname')
        sys.exit(1)

    add_user(cur, options.serial, options.keyfile, options.name, \
            options.surname)
    conn.commit()


def add_user(cur, serial, keyfile, name, surname, nickname=None, \
             lastValid=None, firstValid=None):
    field = ['serial', 'pubkey', 'name', 'surname']
    value = [serial, get_key(keyfile), name, surname]

    if nickname:
        field.append('nickname')
        value.append(nickname)

    if lastValid:
        field.append('lastValid')
        value.append(lastValid)

    if firstValid:
        field.append('firstValid')
        value.append(firstValid)

    field_list = ','.join(field)
    questionmarks = "?" * (len(field))
    questionmarks = ','.join(questionmarks)
    cur.execute('INSERT INTO user(' + field_list +') VALUES (' + \
                questionmarks + ')', value)


def get_key(keyfile):
    f = open(keyfile, 'r')
    key = f.read()
    f.close()

    key = key.strip()
    return key


def get_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    return cur, conn


def serial_exists(serial, cur):
    cur.execute('SELECT * FROM user WHERE serial = ?', (serial,))
    ret = cur.fetchone()

    if not ret:
        return False
    else:
        return True


if __name__ == '__main__':
    main()
