#!/usr/bin/env python2
#-*- coding: utf-8 -*-
"""generate authorized_keys file from sqlite3 database"""
import sqlite3


DATABASE = 'shackspacekey.sqlite'
OUTFILE = 'authorized_keys'


def main():
    """does the job"""
    conn = open_database(DATABASE)
    cur = conn.cursor()
    dataset = get_dataset(cur)
    tasks = ['open', 'close']

    for task in tasks:
        gen_keyfile(dataset, task)

    conn.close()


def get_dataset(cur):
    """pulls a dataset from the sqlite3 DB
    returns array of dict"""

    dataset = []
    cur.execute('SELECT * FROM user')
    ret = cur.fetchall()

    for r in ret:
        #check the database schema to get the order
        serial = r[0]
        name = r[1]
        surname = r[2]
        nick = r[3]
        created = r[4]
        first_valid = r[5]
        last_valid = r[6]
        pubkey = r[7]

        dataset.append({'serial': serial,
                        'name': name,
                        'surname': surname,
                        'nickname': nick,
                        'created': created,
                        'firstValid': first_valid,
                        'lastValid': last_valid,
                        'pubkey': pubkey})
    return dataset


def open_database(database):
    """establishes connection to DB
    returns connection"""
    conn = sqlite3.connect(database)
    return conn


def gen_keyfile(dataset, task):
    """takes the data and builds a keyfile"""
    filename = OUTFILE
    filename += '.' + task

    f = open(filename, 'w')
    security_options = "no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty"
    command = '/var/portal' + task + '/' + task + ' '


    for keymember in dataset:
        parameter = []
        parameter.append("-s")
        parameter.append(str(keymember["serial"]))
        parameter.append("-n")
        parameter.append(keymember["name"] + "_" + keymember["surname"])

        parameterlist = ' '.join(parameter)

        line = "command=\""
        line += command
        line += ' ' + parameterlist
        line += "\"," + security_options + " "
        line += keymember["pubkey"]
        line += "\n"

        f.write(line)

    f.close()


if __name__ == '__main__':
    main()
