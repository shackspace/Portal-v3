#!/bin/sh
#initial bootstrapping script


aptitude -y update
aptitude -y install git hostapd udhcpd python-virtualenv python-dev build-essential


#clone repo
git clone https://github.com/shackspace/Portal-v3.git /opt/Portal-v3


#link config files to /etc
rm /etc/hostapd/hostapd.conf
ln -s /opt/Portal-v3/portal/config/hostapd/hostapd.conf /etc/hostapd/hostapd.conf

rm /etc/default/hostapd
ln -s /opt/Portal-v3/portal/config/default/hostapd /etc/default/hostapd

rm /etc/udhcpd.conf
ln -s /opt/Portal-v3/portal/config/udhcpd.conf /etc/udhcpd.conf

rm /etc/default/udhcpd
ln -s /opt/Portal-v3/portal/config/default/udhcpd /etc/default/udhcpd

rm /etc/network/interfaces
ln -s /opt/Portal-v3/portal/config/network/interfaces /etc/network/interfaces


#restart hostapd and udhcpd
service hostapd restart
service udhcpd restart


#generate env
cd /opt/Portal-v3/portal/gpio
virtualenv ENV


#install requiremnts
. ENV/bin/activate
pip install -r requirements.txt


#add user open
useradd -b /home --create-home open
mkdir /home/open/.ssh
chown open:open /home/open/.ssh
chmod 700 /home/open/.ssh


#add user close
useradd -b /home --create-home close
mkdir /home/close/.ssh
chown close:close /home/close/.ssh
chmod 700 /home/close/.ssh

echo open portal= NOPASSWD: /opt/Portal-v3/portal/gpio/portal.py >> /etc/sudoers
echo close portal= NOPASSWD: /opt/Portal-v3/portal/gpio/portal.py >> /etc/sudoers
