from util import hook, http
from util import http, hook, urlnorm, timesince
from util.siteparse import SiteParse, WebsiteParse, VideoParse

import json
from juggernaut import Juggernaut
import datetime


jug = Juggernaut()

url_re = r'(((https?):\/\/)|www\.)(([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)|localhost|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.(com|net|org|info|biz|gov|name|edu|[a-zA-Z][a-zA-Z]))(:[0-9]+)?((\/|\?)[^"]*[^,;\.:">)])?'

all_re = r'.*'



def parse_link(link):
    parse = SiteParse(link)

    if parse.category == 'image':
        title = "Image"
        thumb = None
        vid = None

    elif parse.category == 'music':
        title = "Audio File"
        thumb = None
        vid = None
    
    elif parse.category == 'video':
        vp = VideoParse(link)
        title = vp.title
        thumb = vp.thumbnail
        vid = vp.id

    else: # url is just a website 
        website = WebsiteParse(link)
        title = website.title
        thumb = None
        vid = None

    return {'category': parse.category, 'title': title, 'url': link, "vid": vid, "thumb": thumb}


def dthandler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable.' % (type(obj), repr(obj))

@hook.regex(url_re)
def poop_url(match, nick='', chan='', bot=None):
    if chan.find('#') == -1:
        return
    else:
        chan = chan.strip('#')

    if chan == "thesite":
        return

    url = urlnorm.normalize(match.group().encode('utf-8'))
    url = url.decode('utf-8')

    plink = parse_link(url)
    plink['nick'] = nick
    plink['chan'] = chan

    data = json.dumps(plink)
    jug.publish('links', data)


#@hook.regex(all_re)
#def log_chat(match, nick='', chan='', say=None, bot=None):
#    
#    if chan.find("#") == -1:
#        return 
#    else:
#        chan = chan.strip("#")
#    if chan == "thesite":
#        return
#    
#
#
#
#    data = json.dumps({'date': json.dumps(datetime.datetime.now(), default=dthandler), 'channel': chan, 'nick': nick, 'message': match.group()})
#    jug.publish('links', data)


#@hook.regex(url_re)
#def submit_url(match, nick='', chan='', bot=None):
#   
#    if chan.find("#") == -1:
#        return
#    else:
#        chan = chan.strip('#')
#    
#    if chan == "thesite":
#        return
#
#    url = urlnorm.normalize(match.group().encode('utf-8'))
#    url = url.decode('utf-8')
#    
#    api = slumber.API("http://troutslap.me/api/v1/")
#    api.url.post({"url": url, "nick": nick, "channel": chan}, username=username, api_key=api_key)
