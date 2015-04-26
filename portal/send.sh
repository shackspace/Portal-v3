#!/bin/bash

KEYHOLDER=$(cat /tmp/keyholder)
STATUS='closed'
ADDRESS='http://10.0.2.10:8080/push'

/opt/Portal-v3/portal/check_status.py
if [ $? -eq 0 ] ; then STATUS='open'; fi;

curl -X POST $IP -d '{"status":"'$STATUS'", "keyholder": "'$KEYHOLDER'"}' -H "Content-type: application/json" $ADDRESS
