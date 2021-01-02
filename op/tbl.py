# OPBOT - operbot (tbl.py)
#
# this file is placed in the public domain

"tables (tbl)"

import op

#:
names = op.Ol({
         "bus": ["op.hdl.Bus"], 
         "cfg": ["op.Cfg"],
         "command": ["op.hdl.Command"],
         "default": ["op.Default"], 
         "event": ["op.hdl.Event"],
         "handler": ["op.hdl.Handler"],
         "log": ["op.cmd.Log"],
         "object": ["op.Object"],
         "ol": ["op.Ol"],
         "repeater": ["op.clk.Repeater"],
         "timer": ["op.clk.Timer"],
         "todo": ["op.cmd.Todo"],
         "user": ["op.usr.User"],
         "users": ["op.usr.Users"]
        })
