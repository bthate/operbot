# OP - object programming (test_tinder.py)
#
# this file is placed in the public domain

"run all commands"

# imports

import os, sys ; sys.path.insert(0, os.getcwd())

import op
import os
import random
import sys
import time
import unittest

# defines

cfg = op.prs.parse_cli()
verbose = "v" in cfg.opts
index = cfg.index

param = op.Object()
param.add = ["test@shell", "bart"]
param.dne = ["test4", ""]
param.edt = ["opbot.rss.Cfg", "opbot.rss.Cfg server=localhost", "opbot.rss.Cfg channel=#dunkbots"]
param.rm = ["reddit", ]
param.dpl = ["reddit title,summary,link",]
param.log = ["test1", ""]
param.flt = ["0", "1", ""]
param.fnd = ["cfg server==localhost", "kernel wd", "rss rss==reddit rss", "email From==pvp From Subject -t"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]
param.mbx = ["~/Desktop/25-1-2013", ""]

events = []
ignore = ["mbx", "rss"]
nrtimes = 1

# classes

class TestHandler(op.hdl.Handler):

     def direct(self, txt):
         if verbose:
             print(txt)

class Command(op.hdl.Command):

    def direct(self, txt):
        if verbose:
            print(txt)

class Test_Tinder(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(index or 1):
            op.thr.launch(tests, h)
        consume(events)

    def test_neuman(self):
        for x in range(index or 1):
            tests(h)

    def test_sorted(self):
        for x in range(index or 1):
            sortedtests(h)

# functions
        
def consume(elems):
    fixed = []
    res = []
    for e in elems:
        r = e.wait()
        res.append(r)
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue
    h.stop()
    return res
    
def sortedtests(b):
    keys = sorted(h.cmds)
    for cmd in keys:
        if cmd in ignore:
            continue
        events.extend(do_cmd(cmd))

def tests(b):
    keys = list(h.cmds)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ignore:
            continue
        events.extend(do_cmd(cmd))

def do_cmd(cmd):
    exs = op.get(param, cmd, [""])
    e = list(exs)
    random.shuffle(e)
    events = []
    nr = 0
    for ex in e:
        nr += 1
        txt = cmd + " " + ex 
        e = Command(txt)
        h.put(e)
        events.append(e)
    return events

# runtime

h = TestHandler()
h.register("cmd", op.hdl.cmd)
h.load("op.cmd")
h.start()

for e in do_cmd("mbx"):
    e.wait()

for e in do_cmd("rss https://www.reddit.com/r/python/.rss"):
    e.wait()
