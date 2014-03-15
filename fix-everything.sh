#!/bin/sh
#initial bootstrapping script

#create users and group
groupadd openclose
useradd -b /var/portal -G openclose -m open
useradd -b /var/portal -G openclose -m close

#set permissions
chgrp -R openclose /var/portal/open
chgrp -R openclose /var/portal/close

#set permissions to access.log
touch /var/portallog/access.log
chgrp openclose /var/portallog/access.log
chmod -R 775 /var/portallog

#execute GPIO-init script
./init.sh
