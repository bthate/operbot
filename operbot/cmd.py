# OPBOT - operbot (cmd.py)
#
# this file is placed in the public domain

"opbot commands (cmd)"

# imports

import op
import opbot
import threading
import time

# defines

def __dir__():
    return ("cfg", "dpl", "dne", "ftc", "rem", "rss", "ver")

# commands

def cfg(event):
    "configure irc (cfg)"
    c = opbot.irc.Cfg()
    op.dbs.last(c)
    if not event.prs.sets:
        return event.reply(op.format(c, skip=["username", "realname"]))
    op.update(c, event.prs.sets)
    op.save(c)
    event.reply("ok")

def dpl(event):
    "set keys to display (dpl)"
    if len(event.args) < 2:
        return
    setter = {"display_list": event.args[1]}
    for fn, o in op.dbs.last_match("opbot.rss.Rss", {"rss": event.args[0]}):
        op.edit(o, setter)
        op.save(o)
        event.reply("ok")

def ftc(event):
    "run a fetch (ftc)"
    res = []
    thrs = []
    fetcher = opbot.rss.Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply("fetched %s" % ",".join([str(x) for x in res]))
        return

def rem(event):
    "remove a rss feed (rem)"
    if not event.args:
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for fn, o in op.dbs.find("opbot.rss.Rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        op.save(o)
    event.reply("ok")

def rss(event):
    "add a rss feed (rss)"
    if not event.args:
        return
    url = event.args[0]
    res = list(op.dbs.find("opbot.rss.Rss", {"rss": url}))
    if res:
        return
    o = opbot.rss.Rss()
    o.rss = event.args[0]
    op.save(o)
    event.reply("ok")

def ver(event):
    "show version (ver)"
    event.reply("OPBOT %s - operbot" % op.__version__)
