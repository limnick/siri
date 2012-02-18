import re
import random
import urllib2
from util import hook, http

class Fourchan:

    def __init__(self):
        """Crude regex's which will eventually break"""
        self.pages = re.compile(r"""\[<a href="\d{1,2}\.html?">(\d{1,2})</a>\]""")
        self.links = re.compile(r"""File\s*:\s*<a href="(.*src/\d.+\.jpg)" target="_blank">\d.+\.jpg.+?</a>""")
        self.boardNames = []
        self.linkList = []

    def fetch(self):
        infile = urllib2.urlopen('http://cgi.4chan.org/a/imgboard.html')
        listFile = infile.read()
        infile.close()
        self.linkList = self.links.findall(listFile)

    def getImage(self):
        return self.linkList[random.randrange(len(self.linkList))]

#if __name__ == "__main__":

#    fourchan = Fourchan()
#    fourchan.fetch()
#    print fourchan.getImage()

@hook.command('anime')
@hook.command
def chan(inp, reply=None, say=None, nick=''):
   fourchan = Fourchan()
   fourchan.fetch()
   if inp=='':   
      say(fourchan.getImage())
   else:
      say(fourchan.getImage())
