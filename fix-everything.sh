
#initial bootstrapping script
#creates users and shit.
echo "open:x:1338:1338:open the door,,,:/var/portal/open:/var/portal/open/open.sh" >>/etc/passwd
echo "close:x:1338:1338:close the door,,,:/var/portal/close:/var/portal/close/close.sh" >>/etc/passwd
echo "openclose:x:1338:" >>/etc/group

echo "/var/portal/open/open.sh" >>/etc/shells
echo "/var/portal/close/close.sh" >>/etc/shells

chown -R open:openclose /var/portal/open
chown -R open:openclose /var/portal/close

touch /var/portal/access.log
chown open:openclose /var/portal/access.log

cat /var/portal/motd >/etc/banner
