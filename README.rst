README
######

Welcome to OPBOT,

OPBOT is a pure python3 IRC chat bot that can run as a background daemon
for 24/7 a day presence in a IRC channel. It installs itself as a service so
you can get it restarted on reboot. You can use it to display RSS feeds, act as a
UDP to IRC gateway, program your own commands for it, have it log objects on
disk and search them and scan emails for correspondence analysis. OPBOT uses
a JSON in file database with a versioned readonly storage. It reconstructs
objects based on type information in the path and uses a "dump OOP and use
OP" programming library where the methods are factored out into functions
that use the object as the first argument.

OPBOT is placed in the Public Domain, no COPYRIGHT, no LICENSE.

INSTALL
=======

installation is through pypi:

::

 > sudo pip3 install opbot

MODULES
=======

OPBOT provides the following modules:

::

    opbot.irc          - internet relay chat
    opbot.rss          - rich site syndicate
    opbot.udp          - udp to irc relay

OPCTL
=====

OPBOT has it's own CLI, the opctl program. It needs root because OPBOT
program uses systemd to get it started after a reboot. You can run it on the shell
prompt and, as default, it won't do anything.

:: 

 $ sudo opctl
 $ 

you can use opctl <cmd> to run a command directly, use the cmd command to see a list of commands:

::

 $ sudo opctl cmd
 cfg,cmd,dne,dpl,fnd,ftc,log,mbx,rem,rss,tdo,tsk,udp,upt,ver


IRC
===

configuration is done with the cfg command:

::

 $ sudo opctl cfg
 channel=#opbot nick=opbot port=6667 server=localhost

you can use setters to edit fields in a configuration:

::

 $ sudo opctl cfg server=irc.freenode.net channel=\#dunkbots nick=opbot
 ok

then restart the opbot service:

::

 $ sudo service opbot restart

RSS
===

OPBOT provides with the use of feedparser the possibility to server rss
feeds in your channel. To add an url use the rss command with an url:

::

 $ sudo opctl rss https://github.com/bthate/opbot/commits/master.atom
 ok 1

run the rss command to see what urls are registered:

::

 $ sudo opctl fnd rss
 0 https://github.com/bthate/opbot/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds:

::

 $ sudo opctl ftc
 fetched 20

adding rss to mods= will load the rss module and start it's poller.

::

 $ sudo bot mods=irc,rss

UDP
===

OPBOT also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed on the channel.

adding the udp to mods= load the udp to irc gateway

::

 $ sudo opbot mods=irc,udp

use the 'opudp' command to send text via the bot to the channel on the irc server:

::

 $ tail -f /var/log/syslog | opudp

output to the IRC channel can be done with the use python3 code to send a UDP packet 
to OPBOT, it's unencrypted txt send to the bot and display on the joined channels.

to send a udp packet to OPBOT in python3:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)


SERVICE
=======

if you want to run the bot 24/7 you can install OPBOT as a service for
the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/opbot.service file:

::

 [Unit]
 Description=OPBOT - operbot
 After=network-online.target

 [Service]
 DynamicUser=True
 StateDirectory=opbot
 LogsDirectory=opbot
 CacheDirectory=opbot
 ExecStart=/usr/local/bin/opd
 CapabilityBoundingSet=CAP_NET_RAW

 [Install]
 WantedBy=multi-user.target

then enable the opbot service with:

::

 $ sudo systemctl enable opbot
 $ sudo systemctl daemon-reload

to configure OPBOT use the cfg (config) command (see above). use sudo for the system
daemon and without sudo if you want to run the bot locally. then restart
the opbot service.

::

 $ sudo service opbot stop
 $ sudo service opbot start

if you don't want opbot to startup at boot, remove the service file:

::

 $ sudo rm /etc/systemd/system/opbot.service


CONTACT
=======

"contributed back to society"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots at irc.freenode.net
