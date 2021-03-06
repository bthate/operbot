# OPERBOT - operbot (udp.py)
#
# this file is placed in the public domain

"udp to irc relay (udp)"

import op
import select
import socket
import sys
import time

def init(hdl):
    "udp to irc relay"
    u = UDP()
    return op.thr.launch(u.start)

class Cfg(op.Cfg):

    "configuration"

    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.port = 5500

class UDP(op.Object):

    "udp to irc relay"

    def __init__(self):
        super().__init__()
        self.stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()
        self.cfg = Cfg()

    def output(self, txt, addr):
        "message on bus"
        op.hdl.Bus.announce(txt.replace("\00", ""))

    def server(self):
        "loop"
        try:
            self._sock.bind((self.cfg.host, self.cfg.port))
        except (socket.gaierror, OSError):
            return
        while not self.stopped:
            (txt, addr) = self._sock.recvfrom(64000)
            if self.stopped:
                break
            data = str(txt.rstrip(), "utf-8")
            if not data:
                break
            self.output(data, addr)

    def exit(self):
        "udp to irc relay"
        self.stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(bytes("exit", "utf-8"), (self.cfg.host, self.cfg.port))

    def start(self):
        "udp to irc relay"
        op.dbs.last(self.cfg)
        op.thr.launch(self.server)

def toudp(host, port, txt):
    "send text to udp to irc relay"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))
