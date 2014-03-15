#!/bin/sh

trap "rm /tmp/portal.lock" EXIT

# Check for lockfile
if [ -f /tmp/portal.lock ]
 then
  otherpid=`cat /tmp/portal.lock`
  while [ -e /proc/${otherpid} ]
   do
    sleep 1
   done
  rm -f /tmp/portal.lock
fi

echo $$> /tmp/portal.lock 

rightnow=`date`

#toggle close pin
gpio write 1 0
sleep 1
gpio write 1 1

echo "CLOSE $rightnow ${1} ${2}" >> /var/portallog/access.log

exit
