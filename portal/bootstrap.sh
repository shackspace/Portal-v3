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

#restart hostapd and udhcpd
service hostapd restart
service udhcpd restart
service bind9 restart


#generate env
cd /opt/Portal-v3/portal/gpio
virtualenv ENV


#install requiremnts
. ENV/bin/activate
pip install -r requirements.txt


#add user open
useradd -b /home --create-home -G dialout open
mkdir /home/open/.ssh
chown open:open /home/open/.ssh
chmod 700 /home/open/.ssh


#add user close
useradd -b /home --create-home -G dialout close
mkdir /home/close/.ssh
chown close:close /home/close/.ssh
chmod 700 /home/close/.ssh

#echo open portal= NOPASSWD: /opt/Portal-v3/portal/gpio/portal.py >> /etc/sudoers
#echo close portal= NOPASSWD: /opt/Portal-v3/portal/gpio/portal.py >> /etc/sudoers
