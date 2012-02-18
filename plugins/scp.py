from util import hook, http
import threading
from time import sleep
import sqlite3
import re
import os
class SCPThread(threading.Thread):
    def __init__(self, dbpath):
        threading.Thread.__init__(self, name="SCP")
        self.dbpath = dbpath
    def run(self):
        db = sqlite3.connect(self.dbpath)
        db.execute("create table if not exists scps(number varchar primary key, title varchar)")
        db.text_factory = str
        while True:
            try:
                c = db.cursor()
                c.execute("delete from scps")
                page = http.to_utf8(http.get("http://scp-wiki.wikidot.com/scp-series"))
                scp_re = re.compile(r'<a href="/scp-(.*)">SCP-\1</a> - (.*?)</li>', re.I)
                scp_list = scp_re.findall(page)
                for (k, v) in scp_list:
                    print k, v
                    c.execute(u"replace into scps(number, title) values (upper(?), ?)", (k, v))
                db.commit()
                c.close()
            except Exception as e:
                print "ERROR ERROR ERROR, ", e
            sleep(60 * 5)

def scp_lookup(number,  title=None):
    url = "http://scp-wiki.wikidot.com/scp-%s" % number
    db = sqlite3.connect(scp_path)
    if not title:
        try: title = db.execute("select title from scps where number = ?", (number.upper(),)).fetchone()[0]
        except TypeError: title = "[ACCESS DENIED]"
    return "%s - %s" % (url, title)

def scp_init(dbpath):
    if all([thread.name != "SCP" for thread in threading.enumerate()]):
        scp_thread = SCPThread(scp_path)
        scp_thread.start()
        sleep(1)

@hook.regex(r'^SCP-((?:\d|-|J)+)$', re.I)
def scp(inp, bot=None, input=None):
    try: inp = inp.groups()[0]
    except AttributeError: pass

    #dbpath = os.path.join(bot.persist_dir, "%s.%s.db" % (input.conn.nick, input.conn.server))
    dbpath = "/home/jewtron/skybot/persist/catteproject.fjord.no.eu.synirc.net.db"
    return scp_lookup(inp)


@hook.event('PRIVMSG')
def multiscp(inp, bot=None, db=None, input=None):
    scps = re.compile('!SCP-((?:\d|-|J)+)', re.I).findall(inp[1])

    #dbpath = os.path.join(bot.persist_dir, "%s.%s.db" % (input.conn.nick, input.conn.server))
    dbpath = "/home/jewtron/skybot/persist/catteproject.fjord.no.eu.synirc.net.db"

    for scp in scps:
        input.reply(scp_lookup(scp))

@hook.command
def rating(inp):
    if "scp-" not in inp: inp = "scp-" + inp
    page = http.get("http://scp-wiki.wikidot.com/%s" % inp)
    rating = http.get_html("http://scp-wiki.wikidot.com/%s" % inp).xpath("//*[@id='prw54353']/text()")[0]
    return rating

@hook.command
def search(inp, db=None):
    inp = "%" + inp + "%"
    scps =  db.execute("SELECT NUMBER, TITLE FROM scps WHERE TITLE LIKE ?", (inp,)).fetchall()
    if len(scps) == 1:
        (number, title) = scps[0]
        return "SCP-%s - %s - http://scp-wiki.wikidot.com/scp-%s" % (number, title, number)
    printed = scps[:5]
    output = ""
    for (number, title) in printed:
        output += "SCP-%s (%s), " % (number, title)
    if len(scps) > 5: output += " plus %d more" % (len(scps) - 5)
    else: output = output[:-2]
    if not output: return "No SCPs found."
    return output

@hook.command
def random(inp, db=None):
    (number, title)  = db.execute("SELECT NUMBER, TITLE FROM scps ORDER BY RANDOM() LIMIT 1").fetchone()
    return "SCP-%s - %s - http://scp-wiki.wikidot.com/scp-%s" % (number, title, number)


def tag(inp):
    return "http://scp-wiki.wikidot.com/system:page-tags/tag/" + inp    
mydir = dir()
scp_path = "/home/jewtron/skybot/persist/scp.db"
#scp_path = os.path.join(os.path.abspath('persist'), "scp.db")
