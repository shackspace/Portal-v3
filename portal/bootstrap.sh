#!/bin/sh
#initial bootstrapping script

#cd to where the script is
cd $(dirname $0)

#create users and group
groupadd openclose
mkdir /
useradd -b /home -G openclose -m open
useradd -b /home -G openclose -m close

#set permissions
chgrp -R openclose /home/open
chgrp -R openclose /home/close

#get most recent stuff from github
git pull

#symlink open.sh and close.sh
ln -s ./open/open.sh /home/open/open.sh
ln -s ./close/close.sh /home/close/close.sh

#set permissions to open.sh and close.sh
chown open:openclose /home/open/open.sh
chown close:openclose /home/close/close.sh
chmod 774 /home/open/open.sh
chmod 774 /home/close/close.sh

#set permissions to access.log
touch /var/portallog/access.log
chgrp openclose /homelog/access.log
chmod -R 775 /var/portallog

#execute GPIO-init script
./init.sh
