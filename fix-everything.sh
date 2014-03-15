#!/bin/sh
#initial bootstrapping script

#create users and group
groupadd openclose
useradd -b /var/portal -G openclose -m open
useradd -b /var/portal -G openclose -m close

#set permissions
chgrp -R openclose /var/portal/open
chgrp -R openclose /var/portal/close

#symlink open.sh and close.sh
ln -s /root/portalv3/software/open/open.sh /var/portal/open/open.sh
ln -s /root/portalv3/software/close/close.sh /var/portal/close/close.sh

#set permissions to open.sh and close.sh
chown open:openclose /var/portal/open/open.sh
chown close:openclose /var/portal/close/close.sh
chmod 774 /var/portal/open/open.sh
chmod 774 /var/portal/close/close.sh

#set permissions to access.log
touch /var/portallog/access.log
chgrp openclose /var/portallog/access.log
chmod -R 775 /var/portallog

#execute GPIO-init script
./init.sh
