import urllib, urllib2, cookielib
import mechanize
import lxml.html as poop
from util import hook, http

def preDBLookup(cat):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    try:
        r = br.open("http://orlydb.com/?q=%s" % (cat))
    except:
        return "Pre DB is Down. Or something."

    parseHtml = poop.fromstring(r.read())
    try: 
        timestamp = parseHtml.xpath("//div[@id='releases']/div[1]/span[1][@class='timestamp']/text()")[0]
    except:
        return "Can't find what you're lookin for bro. Try something less gay."
    splitstamp = timestamp.split(" ")
    time = splitstamp[1]
    date = splitstamp[0]

    category = parseHtml.xpath("//div[@id='releases']/div[1]/span[2][@class='section']/a/text()")[0]
    name = parseHtml.xpath("//div[@id='releases']/div[1]/span[3][@class='release']/text()")[0]
    try:
        size = parseHtml.xpath("//div[@id='releases']/div[1]/span[4][@class='inforight']/span[@class='info']/text()")[0] + "iles"
    except:
        return "Can't find what you're lookin for bro. Try something less gay."
    return ("%s - %s - %s :: %s" % (date, category, name, size))

@hook.command
def predb(inp, nick='', chan='', say=None):
    input = urllib.quote_plus(inp)
    say(preDBLookup(input))

if __name__ == "__main__":
    print preDBLookup("")
