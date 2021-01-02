# OPERBOT - operbot (rss.py)
#
# this file is placed in the public domain

"rich site syndicate (rss)"

# imports

import datetime
import op
import os
import random
import re
import time
import urllib

from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

# defines

def __dir__():
    return ("Cfg", "Rss", "Feed", "Fetcher", "init")

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

def init(hdl):
    "start a rss poller"
    f = Fetcher()
    return op.thr.launch(f.start)

# classes

class Cfg(op.Cfg):

    "rss configuration"

    def __init__(self):
        super().__init__()
        self.dosave = True

class Feed(op.Default):

    "feed item"

class Rss(op.Object):

    "rss feed url"

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(op.Object):

    "all urls seen"

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(op.Object):

    "rss feed poller"

    cfg = Cfg()
    seen = Seen()

    def display(self, o):
        "display a rss feed item"
        result = ""
        dl = []
        try:
            dl = o.display_list.split(",")
        except AttributeError:
            pass
        if not dl:
            dl = self.cfg.display_list.split(",")
        if not dl or not dl[0]:
            dl = ["title", "link"]
        for key in dl:
            if not key:
                continue
            data = op.get(o, key, None)
            if not data:
                continue
            if key == "link" and self.cfg.tinyurl:
                datatmp = get_tinyurl(data)
                if datatmp:
                    data = datatmp[0]
            data = data.replace("\n", " ")
            data = op.utl.strip_html(data.rstrip())
            data = op.utl.unescape(data)
            result += data.rstrip()
            result += " - "
        return result[:-2].rstrip()

    def fetch(self, rssobj):
        "rss feed"
        counter = 0
        objs = []
        if not rssobj.rss:
            return 0
        for o in reversed(list(get_feed(rssobj.rss))):
            if not o:
                continue
            f = Feed()
            op.update(f, rssobj)
            op.update(f, op.O(o))
            u = urllib.parse.urlparse(f.link)
            if u.path and not u.path == "/":
                url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
            else:
                url = f.link
            if url in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(url)
            counter += 1
            objs.append(f)
            if self.cfg.dosave:
                op.save(f)
        if objs:
            op.save(Fetcher.seen)
        for o in objs:
            txt = self.display(o)
            op.hdl.Bus.announce(txt)
        return counter

    def run(self):
        "all feeds"
        thrs = []
        for fn, o in op.dbs.all("operbot.rss.Rss"):
            thrs.append(op.thr.launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        "rss poller"
        op.dbs.last(Fetcher.cfg)
        op.dbs.last(Fetcher.seen)
        if repeat:
            repeater = op.clk.Repeater(300.0, self.run)
            repeater.start()

    def stop(self):
        "rss poller"
        op.save(self.seen)

# functions

def get_feed(url):
    "feed"
    if op.debug:
        return [op.Object(), op.Object()]
    try:
        result = op.utl.get_url(url)
    except (HTTPError, URLError):
        return [op.Object(), op.Object()]
    if gotparser:
        result = feedparser.parse(result.data)
        if "entries" in result:
            for entry in result["entries"]:
                yield entry
    else:
        return [op.Object(), op.Object()]
