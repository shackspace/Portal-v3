#!/bin/bash

KEYHOLDER=$(cat /tmp/keyholder)
STATUS='closed'
ADDRESS='http://127.0.0.1/push'

/opt/Portal-v3/portal/gpio/check_status.py
if [ $? -eq 0 ] ; then STATUS='open'; fi;

curl -X POST $IP -d '{"status":"'$STATUS'", "nick": "'$KEYHOLDER'"}' -H "Content-type: application/json" $ADDRESS
