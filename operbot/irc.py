# OPERBOT - operbot (irc.py)
#
# this file is placed in the public domain

"internet relay chat (irc)"

# imports

import op
import os
import queue
import socket
import textwrap
import time
import threading
import _thread

# defines

def __dir__():
    return ("Cfg", "DCC", "Event", "IRC", "init")

def init(hdl):
    "create a irc bot and return it"
    i = IRC()
    i.clone(hdl)
    return op.thr.launch(i.start)

# locks

saylock = _thread.allocate_lock()

# classes

class Cfg(op.Cfg):

    "configuration object"

    def __init__(self):
        super().__init__()
        self.channel = "#operbot"
        self.nick = "operbot"
        self.server = "localhost"
        self.username = "operbot"
        self.realname = "operbot"

class Event(op.hdl.Event):

    "irc event"

class TextWrap(textwrap.TextWrapper):

    "text wrapper"

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 450

class IRC(op.hdl.Handler):

    "irc bot"

    def __init__(self):
        super().__init__()
        self._buffer = []
        self._connected = threading.Event()
        self._joined = threading.Event()
        self._outqueue = queue.Queue()
        self._sock = None
        self._fsock = None
        self._trc = ""
        self.cc = "!"
        self.cfg = Cfg()
        self.cmds = op.Object()
        self.channels = []
        self.register("cmd", op.hdl.cmd)
        self.register("ERROR", self.ERROR)
        self.register("LOG", self.LOG)
        self.register("NOTICE", self.NOTICE)
        self.register("PRIVMSG", self.PRIVMSG)
        self.register("QUIT", self.QUIT)
        self.register("366", self.JOINED)
        self.speed = "slow"
        self.state = op.Object()
        self.state.needconnect = False
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrconnect = 0
        self.state.nrerror = 0
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.threaded = False
        self.verbose = False
        self.users = op.usr.Users()

    def _connect(self, server):
        "connect (blocking) to irc server"
        oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oldsock.setblocking(1)
        oldsock.settimeout(5.0)
        try:
            oldsock.connect((server, 6667))
        except (OSError, ConnectionError):
            time.sleep(2.0)
            try:
                oldsock.connect((server, 6667))
            except (OSError, ConnectionError):
                self._connected.set()
                return False
        oldsock.setblocking(1)
        oldsock.settimeout(1200.0)
        self._sock = oldsock
        self._fsock = self._sock.makefile("r")
        fileno = self._sock.fileno()
        os.set_inheritable(fileno, os.O_RDWR)
        self._connected.set()
        return True

    def _parsing(self, txt):
        "into an event"
        rawstr = str(txt)
        rawstr = rawstr.replace("\u0001", "")
        rawstr = rawstr.replace("\001", "")
        o = Event()
        o.rawstr = rawstr
        o.orig = repr(self)
        o.command = ""
        o.arguments = []
        arguments = rawstr.split()
        if arguments:
            o.origin = arguments[0]
        else:
            o.origin = self.cfg.server
        if o.origin.startswith(":"):
            o.origin = o.origin[1:]
            if len(arguments) > 1:
                o.command = arguments[1]
                o.type = o.command
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.count(":") <= 1 and arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        o.arguments.append(arg)
                o.txt = " ".join(txtlist)
        else:
            o.command = o.origin
            o.origin = self.cfg.server
        try:
            o.nick, o.origin = o.origin.split("!")
        except ValueError:
            o.nick = ""
        target = ""
        if o.arguments:
            target = o.arguments[-1]
        if target.startswith("#"):
            o.channel = target
        else:
            o.channel = o.nick
        if not o.txt:
            if rawstr[0] == ":":
                rawstr = rawstr[1:]
            o.txt = rawstr.split(":", 1)[-1]
        if not o.txt and len(arguments) == 1:
            o.txt = arguments[1]
        spl = o.txt.split()
        if len(spl) > 1:
            o.args = spl[1:]
        return o

    @op.utl.locked(saylock)
    def _say(self, channel, txt):
        "on a channel"
        wrapper = TextWrap()
        txt = str(txt).replace("\n", "")
        for t in wrapper.wrap(txt):
            if not t:
                continue
            self.command("PRIVMSG", channel, t)
            if (time.time() - self.state.last) < 4.0:
                time.sleep(4.0)
            self.state.last = time.time()

    def _some(self):
        "blocking read"
        inbytes = self._sock.recv(512)
        txt = str(inbytes, "utf-8")
        if txt == "":
            raise ConnectionResetError
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for s in splitted[:-1]:
            self._buffer.append(s)
        self.state.lastline = splitted[-1]

    def announce(self, txt):
        "annouce text"
        for channel in self.channels:
            self.say(channel, txt)

    def command(self, cmd, *args):
        "send a command"
        if not args:
            self.raw(cmd)
            return
        if len(args) == 1:
            self.raw("%s %s" % (cmd.upper(), args[0]))
            return
        if len(args) == 2:
            self.raw("%s %s :%s" % (cmd.upper(), args[0], " ".join(args[1:])))
            return
        if len(args) >= 3:
            self.raw("%s %s %s :%s" % (cmd.upper(), args[0], args[1], " ".join(args[2:])))
            return

    def connect(self, server, nick):
        "connect to server"
        nr = 0
        while not self.stopped:
            self.state.nrconnect += 1
            if self._connect(server):
                break
            time.sleep(10.0)
            nr += 1
        else:
            self._connected.set()
        self._connected.wait()
        self.logon(server, nick)

    def handle(self, event):
        "invoke callback"
        if event.command in self.cbs:
            self.cbs[event.command](event)

    def doconnect(self):
        "start input/output tasks"
        assert self.cfg.server
        assert self.cfg.nick
        super().start()
        self.connect(self.cfg.server, self.cfg.nick)
        op.thr.launch(self.input)
        op.thr.launch(self.output)

    def input(self):
        "loop for input"
        while not self.stopped:
            try:
                e = self.poll()
            except (OSError, ConnectionResetError, socket.timeout) as ex:
                e = op.hdl.Event()
                e.error = str(ex)
                self.ERROR(e)
                break
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            self.handle(e)

    def joinall(self):
        "all channels"
        for channel in self.channels:
            self.command("JOIN", channel)

    def logon(self, server, nick):
        "do logon handshake"
        self._connected.wait()
        assert self.cfg.username
        assert self.cfg.realname
        self.raw("NICK %s" % nick)
        self.raw("USER %s %s %s :%s" % (self.cfg.username, server, server, self.cfg.realname))

    def output(self):
        "loop for output"
        while 1:
            channel, txt = self._outqueue.get()
            if channel is None:
                break
            if txt:
                time.sleep(0.001)
                self._say(channel, txt)

    def poll(self):
        "block on socket"
        self._connected.wait()
        if not self._buffer:
            self._some()
        if not self._buffer:
            return self._parsing("")
        e = self._parsing(self._buffer.pop(0))
        cmd = e.command
        if cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", e.txt or "")
        elif cmd == "PONG":
            self.state.pongcheck = False
        if cmd == "001":
            self.state.needconnect = False
            if "servermodes" in dir(self.cfg):
                self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
            self.joinall()
        elif cmd == "366":
            self._joined.set()
        elif cmd == "433":
            nick = self.cfg.nick + "_"
            self.cfg.nick = nick
            self.raw("NICK %s" % self.cfg.nick or "operbot")
        return e

    def raw(self, txt):
        "send on raw socket"
        txt = txt.rstrip()
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        self._connected.wait()
        try:
            self._sock.send(txt)
        except (OSError, ConnectionResetError) as ex:
            e = Event()
            e.error = str(ex)
            self.LOG(e)
            self._connected.clear()
        self.state.last = time.time()
        self.state.nrsend += 1

    def say(self, channel, txt):
        "forward to output loop"
        self._outqueue.put_nowait((channel, txt))

    def start(self, cfg=None):
        "connect to server"
        if cfg is not None:
            op.update(self.cfg, cfg)
        else:
            op.dbs.last(self.cfg)
        assert self.cfg.channel
        assert self.cfg.server
        self.channels.append(self.cfg.channel)
        self._joined.clear()
        op.thr.launch(self.doconnect)
        self._joined.wait()

    def stop(self):
        "flush queues and shutdown sockets"
        super().stop()
        self._outqueue.put((None, None))
        try:
            self._sock.shutdown(2)
        except OSError:
            pass

    def ERROR(self, event):
        "do stop/start on error"
        self.state.nrerror += 1
        self.state.error = event.error
        self._connected.clear()
        self.stop()
        self.start()

    def JOINED(self, event):
        "has joined all channels"
        self._joined.set()

    def LOG(self, event):
        "log to console, override this"

    def NOTICE(self, event):
        "respond with version of the okbot"
        from operbot import __version__
        if event.txt.startswith("VERSION"):
            txt = "\001VERSION %s %s - %s\001" % ("OPERBOT", __version__, "operbot")
            self.command("NOTICE", event.channel, txt)

    def PRIVMSG(self, event):
        "forward dcc chat and check for commands"
        if event.txt.startswith("DCC CHAT"):
            if self.cfg.users and not self.users.allowed(event.origin, "USER"):
                return
            try:
                dcc = DCC()
                dcc.encoding = "utf-8"
                dcc.clone(self)
                op.thr.launch(dcc.connect, event)
                return
            except ConnectionError as ex:
                return
        if event.txt and event.txt[0] == self.cc:
            if self.cfg.users and not self.users.allowed(event.origin, "USER"):
                return
            event.type = "cmd"
            event.txt = event.txt[1:]
            super().dispatch(event)

    def QUIT(self, event):
        "stop if self"
        if self.cfg.server in event.orig:
            self.stop()

class DCC(op.hdl.Handler):

    "direct client to client (dcc)"

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._sock = None
        self._fsock = None
        self.encoding = "utf-8"
        self.origin = ""

    def raw(self, txt):
        "send text on the dcc socket"
        self._fsock.write(str(txt).rstrip())
        self._fsock.write("\n")
        self._fsock.flush()

    def announce(self, txt):
        "annouce to dcc console, overload this"

    def connect(self, event):
        "connect to offering socket"
        arguments = event.txt.split()
        addr = arguments[3]
        port = arguments[4]
        port = int(port)
        if ':' in addr:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        s.setblocking(1)
        #os.set_inheritable(s.fileno(), os.O_RDWR)
        self._sock = s
        self._fsock = self._sock.makefile("rw")
        self.raw('Welcome to OPERBOT %s' % event.nick)
        self.origin = event.origin
        op.thr.launch(self.input)
        super().start()
        self._connected.set()

    def input(self):
        "loop for input"
        while 1:
            try:
                e = self.poll()
            except EOFError:
                break
            self.put(e)

    def poll(self):
        "poll (blocking) for input and create an event for it"
        self._connected.wait()
        e = op.hdl.Event()
        e.type = "cmd"
        txt = self._fsock.readline()
        txt = txt.rstrip()
        op.prs.parse(e, txt)
        e._sock = self._sock
        e._fsock = self._fsock
        e.channel = self.origin
        e.origin = self.origin or "root@dcc"
        e.orig = repr(self)
        return e

    def say(self, channel, txt):
        "skip channel and print on socket"
        self.raw(txt)
