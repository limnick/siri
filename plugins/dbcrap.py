from util import hook, http
import threading
from time import sleep
import sqlite3
import re
import sys
import os

if __name__ == "__main__":
    db = sqlite3.connect("/home/jewtron/skybot/persist/catteproject.fjord.no.eu.synirc.net.db")
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
                c.execute(u"replace into scps(number, title) values (upper(?), ?)", (k,v))
            db.commit()
            c.close()
            print "added scps to scp.db :: closing."
            sys.exit()

        except Exception as e:
            print "ERROR ERROR ERROR, ", e
            sleep(60 * 5)

