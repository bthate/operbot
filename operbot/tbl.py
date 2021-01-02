# OPBOT - operbot (tbl.py)
#
# this file is placed in the public domain

"tables (tbl)"

import op

#:
names = op.Ol({
         "bus": ["op.hdl.Bus"], 
         "cfg": ["opbot.udp.Cfg", "op.Cfg", "opbot.irc.Cfg", "opbot.rss.Cfg"],
         "command": ["op.hdl.Command"],
         "dcc": ["opbot.irc.DCC"],
         "default": ["op.Default"], 
         "event": ["opbot.irc.Event", "op.hdl.Event"],
         "feed": ["opbot.rss.Feed"],
         "fetcher": ["opbot.rss.Fetcher"],
         "handler": ["op.hdl.Handler"],
         "irc": ["opbot.irc.IRC"],
         "log": ["op.cmd.Log"],
         "object": ["op.Object"],
         "ol": ["op.Ol"],
         "repeater": ["op.clk.Repeater"],
         "rss": ["opbot.rss.Rss"],
         "timer": ["op.clk.Timer"],
         "todo": ["op.cmd.Todo"],
         "udp": ["opbot.udp.UDP"],
         "user": ["op.usr.User"],
         "users": ["op.usr.Users"]
        })
