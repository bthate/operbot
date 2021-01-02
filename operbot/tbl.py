# OPERBOT - operbot (tbl.py)
#
# this file is placed in the public domain

"tables (tbl)"

import op

#:
names = op.Ol({
         "bus": ["op.hdl.Bus"], 
         "cfg": ["operbot.udp.Cfg", "op.Cfg", "operbot.irc.Cfg", "operbot.rss.Cfg"],
         "command": ["op.hdl.Command"],
         "dcc": ["operbot.irc.DCC"],
         "default": ["op.Default"], 
         "event": ["operbot.irc.Event", "op.hdl.Event"],
         "feed": ["operbot.rss.Feed"],
         "fetcher": ["operbot.rss.Fetcher"],
         "handler": ["op.hdl.Handler"],
         "irc": ["operbot.irc.IRC"],
         "log": ["op.cmd.Log"],
         "object": ["op.Object"],
         "ol": ["op.Ol"],
         "repeater": ["op.clk.Repeater"],
         "rss": ["operbot.rss.Rss"],
         "timer": ["op.clk.Timer"],
         "todo": ["op.cmd.Todo"],
         "udp": ["operbot.udp.UDP"],
         "user": ["op.usr.User"],
         "users": ["op.usr.Users"]
        })
