#!/usr/bin/env python2
#-*- coding: utf8 -*-
"""Deployscript"""

from os import path
import os
from subprocess import call
from sys import exit

AUTHORIZED_KEYS_PREFIX = "authorized_keys"
HOMEPATH = "/home"
HOST = "portal.portal"


def main():
    for state in ['open', 'close']:
        deploy_authorized_keys(state)


def deploy_authorized_keys(state):
    """push the authorized_keys file to the portal

    also fixes filepermissions"""
    filename = '.'.join([AUTHORIZED_KEYS_PREFIX, state])
    if not path.isfile(filename):
        print("'%s' is not a file" % filename)
        exit(1)
    if not os.access(filename, os.R_OK):
        print("'%s' is not readale" % filename)
        exit(2)

    connection = "@".join(["root", HOST])
    destination_path = path.join(HOMEPATH, state, ".ssh", "authorized_keys")
    target = ":".join([connection, destination_path])
    command = ["scp", filename, target]

    ret = call(command)
    if ret > 0:
        print "scp of '%s' failed" % filename
        return ret

    remote_command = ["chown", "-v", ":".join([state, state]), destination_path]
    ret = call(["ssh", connection] + remote_command)
    if ret > 0:
        print "chwon of %s failed" % state
        return ret

    remote_command = ["chmod", "-v", "400", destination_path]
    ret = call(["ssh", connection] + remote_command)
    if ret > 0:
        print "chmod of %s failed" % state
        return ret


if __name__ == "__main__":
    main()
