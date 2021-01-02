README
######

Welcome to OP, short for object programming (op).

OP is a pure python3 object programming library you can use to program
objects with. OP uses a JSON in file database with a versioned readonly storage,
reconstructs objects based on type information in the path and is a "dump OOP 
and use OP" programming library where the methods are factored out into
functions that use an object as the first argument. 

This to provide a clean object, which has no methods to clutter the namespace.
A "clean", still has hidden methods, loadable from JSON file, object that
provides load/save methods to other classes derived from Object.

OP is placed in the Public Domain, no COPYRIGHT, no LICENSE. (:ref:`source <source>`)

INSTALL
=======

installation is through pypi:

::

 > sudo pip3 install op


OBJECT PROGRAMMING
==================

OLIB provides a "move all methods to functions" like this:

::

 obj.method(*args) -> method(obj, *args) 

 e.g.

 not:

 >>> import op
 >>> o = op.Object()
 >>> o.set("key", "value")
 >>> o.key
 'value'

 but:

 >>> import op
 >>> o = op.Object()
 >>> op.set(o, "key", "value")
 >>> o.key
 'value'

MODULES
=======

OP provides the following modules:

::

    op                  - object library
    op.clk              - clock/repeater
    op.cmd              - commands
    op.dbs              - databases
    op.hdl              - handler
    op.prs              - parser
    op.thr              - threads
    op.trm              - terminal
    op.usr              - users
    op.utl              - utilities

CONTACT
=======

"contributed back to society"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net

.. toctree::
    :hidden:
    :glob:

    *
