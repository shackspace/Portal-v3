#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from optparse import OptionParser
from user_mgmt import user_actions
import sys

if __name__ == '__main__':
    if sys.argv[1] == 'list':
        user_actions.list_users()

    elif sys.argv[1] == 'delete':
        user_actions.delete_user(sys.argv[2])

    elif sys.argv[1] == 'add' or sys.argv[1] == 'modify':
        pass

    else:
        print("Usage: user.py [list | add | modify | delete]")
        sys.exit(1)

