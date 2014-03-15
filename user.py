#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from optparse import OptionParser
from user_mgmt import user_actions
import sys

if __name__ == '__main__':
    
    if sys.argv[1] == 'list':
        user_actions.list_users()

    elif sys.argv[1] == 'delete':
        user_actions.del_user(sys.argv[2])

    elif sys.argv[1] == 'add': 
        parser = OptionParser()

        parser.add_option('-k', dest='keyfile')
        parser.add_option('-s', dest='serial')
        parser.add_option('-n', dest='name')
        parser.add_option('-l', dest='surname')
        parser.add_option('--nick', dest='nick', default=None)
        parser.add_option('--first-valid', dest='first', default=None)
        parser.add_option('--last-valid', dest='last', default=None)
    
        (options, args) = parser.parse_args()
        user_actions.add_user(keyfile=options.keyfile, serial=options.serial, \
                              name=options.name, surname=options.surname, \
                              nickname=options.nick, lastValid=options.last, \
                              firstValid=options.first)
        

    elif sys.argv[1] == 'modify':
        pass

    else:
        print("Usage: user.py [list | add | modify | delete]")
        sys.exit(1)

