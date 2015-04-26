#!/bin/sh
#initial bootstrapping script

set -e


aptitude -y update
aptitude -y safe-upgrade
aptitude -y install git hostapd udhcpd python-virtualenv python-dev build-essential bind9


#clone repo
git clone https://github.com/shackspace/Portal-v3.git /opt/Portal-v3


#link config files to /etc
ln -sf /opt/Portal-v3/portal/config/hostapd/hostapd.conf /etc/hostapd/hostapd.conf

ln -sf /opt/Portal-v3/portal/config/default/hostapd /etc/default/hostapd

ln -sf /opt/Portal-v3/portal/config/udhcpd.conf /etc/udhcpd.conf

ln -sf /opt/Portal-v3/portal/config/default/udhcpd /etc/default/udhcpd

ln -sf /opt/Portal-v3/portal/config/network/interfaces /etc/network/interfaces

ln -sf /opt/Portal-v3/portal/config/bind/named.conf.local /etc/bind/named.conf.local

ln -sf /opt/Portal-v3/portal/config/bind/db.portal /etc/bind/db.portal

ln -sf /opt/Portal-v3/portal/config/rc.local /etc/rc.local

#restart hostapd and udhcpd
service hostapd restart
service udhcpd restart
service bind9 restart

#add group portal
groupadd portal

#add user open
useradd -b /home --create-home -G dialout open
mkdir /home/open/.ssh
chown open:open /home/open/.ssh
chmod 700 /home/open/.ssh
gpasswd -a open portal

#add user close
useradd -b /home --create-home -G dialout close
mkdir /home/close/.ssh
chown close:close /home/close/.ssh
chmod 700 /home/close/.ssh
gpasswd -a close portal

#add logging
mkdir -p /var/log/portal/
touch /var/log/portal/portal.log
chgrp -R portal /var/log/portal
chmod -R g+rw portal /var/log/portal

#install push crontab
crontab -l | { cat; echo "* * * * * /opt/Portal-v3/portal/gpio/send.sh"; } | crontab -

#echo open portal= NOPASSWD: /opt/Portal-v3/portal/gpio/portal.py >> /etc/sudoers
#echo close portal= NOPASSWD: /opt/Portal-v3/portal/gpio/portal.py >> /etc/sudoers
