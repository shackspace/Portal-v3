#!/bin/bash
lockfile=/var/run/lock/portal.lock

if [ -f $lockfile ]
then
    age=$(stat -c %Y $lockfile)
    now=$(date +"%s")
    if (( (now - age) > 60 ))
    then
        echo remove lockfile, PID: $(cat $lockfile)
        kill -9 $(cat $lockfile)
        rm $lockfile
    fi
fi
