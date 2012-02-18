#import mechanize
#import sys
#reload(sys)
#sys.setdefaultencoding("latin1")
import os
from util import hook, http
import re
import urllib
from BeautifulSoup import BeautifulSoup
import random

l = list()

def load_fortune(fortune_list, file):
    fortune = ''
    f = open(file, 'r')
    for line in f:
        line = line.strip()
        if line == '%':
            fortune_list.append(fortune)
            fortune = ''
        else:
            if fortune != '':
                fortune += ' '
            fortune += line

files = os.listdir('weedpunk')
for file in files:
    load_fortune(l, 'weedpunk/' + file)
if __name__ == '__main__':
    print __doc__.strip()

@hook.command
def weedpunk(inp, nick='', chan='', say=None):
    say(unicode(random.sample(l, 1)[0]))

