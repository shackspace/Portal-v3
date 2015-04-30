#!/bin/bash

KEYHOLDER=$(cat /var/log/portal/keyholder)
STATUS='closed'
ADDRESS='http://10.0.2.10:8080/push'

/opt/Portal-v3/portal/check_status.py
RET=$?

if [ $RET -eq 1 ]; then
    STATUS='open'; 
elif [ $RET -eq -1 ]; then
    STATUS='unknown';
fi;

curl -X POST -d '{"status":"'$STATUS'", "keyholder": '$KEYHOLDER'}' -H "Content-type: application/json" $ADDRESS
