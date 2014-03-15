#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from optparse import OptionParser
from user_mgmt import user_actions, db_actions
import sys
import sqlite3

def main():
    if len(sys.argv) == 1:
        print_usage()

    if sys.argv[1] == 'list':
        user_actions.list_users()

    elif sys.argv[1] == 'delete':
        user_actions.del_user(sys.argv[2])

    elif sys.argv[1] == 'add':
        parser = OptionParser()

        parser.add_option('-k', dest='keyfile')
        parser.add_option('-u', dest='serial')
        parser.add_option('-n', dest='name')
        parser.add_option('-s', dest='surname')
        parser.add_option('--nick', dest='nick', default=None)
        parser.add_option('--first-valid', dest='first', default=None)
        parser.add_option('--last-valid', dest='last', default=None)

        (options, args) = parser.parse_args()
        user_actions.add_user(keyfile=options.keyfile, serial=options.serial, \
                              name=options.name, surname=options.surname, \
                              nickname=options.nick, lastValid=options.last, \
                              firstValid=options.first)


    elif sys.argv[1] == 'modify':
        parser = OptionParser()

        parser.add_option('-k', dest='keyfile', default=None)
        parser.add_option('-u', dest='serial', default=None)
        parser.add_option('-n', dest='name', default=None)
        parser.add_option('-s', dest='surname', default=None)
        parser.add_option('--nick', dest='nick', default=None)
        parser.add_option('--first-valid', dest='firstValid', default=None)
        parser.add_option('--last-valid', dest='lastValid', default=None)

        (options, args) = parser.parse_args()
        user_actions.mod_user(sys.argv[2], options, args)

    else:
        print_usage()


def print_usage():
    print "Usage: user.py list\n"

    print "       user.py delete <uid>\n"

    print "       user.py add -u <uid> -n <name> -s <surname> [-k <keyfile>]"
    print "                   [--nick <nickname>] [--first-valid <start date>]"
    print "                   [--last-valid <end date, yyyy-mm-dd>]\n"

    print "       user.py modify <uid> [-u <uid>] [-n <name>] [-s <surname>]"
    print "                      [-k <keyfile>] [--nick <nickname>]"
    print "                      [--first-valid <start date, yyyy-mm-dd>]"
    print "                      [--last-valid <end date, yyyy-mm-dd>]"
    sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except sqlite3.OperationalError:
        cur, conn = db_actions.get_db()
        cur.execute("CREATE TABLE user(serial INTEGER PRIMARY KEY, name TEXT, \
                     surname TEXT, nickname TEXT, created timestamp DEFAULT \
                     CURRENT_TIMESTAMP, firstValid timestamp DEFAULT NULL, \
                     lastValid timestampt DEFAULT NULL, pubkey varchar(4096));")
        print "New database created."
        conn.commit()
        conn.close()
        main()

