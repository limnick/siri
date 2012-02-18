from util import hook, http
import bitly
import uuid
from random import randint

api = bitly.Api(login='mumphster', apikey='R_fdf99e81477ce574c386c26560112865')

def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

def random_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@hook.command('gh')
@hook.command
def grouphug(inp, nick='', chan='', say=None):
    if inp == '':
        #h = http.get_html("http://grouphug.us/%s" % str(uuid.uuid1()))
        return "http://grouphug.us/confessions/%s" % str(random_digits(10))
    else:
        h = http.get_html("http://grouphug.us/confessions/%s" % inp)
    hugID = h.xpath('//h2[@class="title"]/a/text()')[1]
    hugContent = removeNonAscii(h.xpath('//div[@class="content"]/p/text()')[1])
    if len(hugContent) > 350:
        hugContent = hugContent[:350] + "..."
    hugURL = "http://grouphug.us/confessions/%s" % (hugID)
    hugLink = api.shorten(hugURL)
    hugOutput = "%s :: \x0307%s\x0F :: \x0308%s\x0F" % (hugContent, hugID, hugLink)
    say(hugOutput)

@hook.command('fml')
@hook.command
def fuckmylife(inp, nick='', chan='', say=None):
    h = http.get_html("http://m.fmylife.com/random/")
    #else:
    # h = http.get_html("http://iphone.fmylife.com/%s") % (inp)
    fmlContent = h.xpath('//p[@class="text"]/text()')[0]
    fmlID = h.xpath('//p[@class="infos"]/a/text()')[0]
    fmlOutput = "%s :: \x0307%s\x0F" % (fmlContent, fmlID, fmlLink)
    say(fmlOutput)

@hook.command('weed')
@hook.command('amnizu')
@hook.command
def thathigh(inp, nick='', chan='', say=None):
    h = http.get_html("http://thathigh.com/random/")
    highContent = h.xpath('//a[@class="storylink"]/text()')[0]
    highOutput = "\x02%s\x0F" % (highContent)
    say(highOutput)
