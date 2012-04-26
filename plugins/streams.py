from util import hook, http
import requests
import redis
import json
from urlparse import urlparse



r = redis.StrictRedis(host='localhost', port=6379, db=0)

def parseURL(urlf):
    o = urlparse(urlf)
    if o.netloc.split('.')[0] == 'www':
        site = o.netloc.split('.')[1]
    else:
        site = o.netloc.split('.')[0]
    if site == 'twitch':
        sid = o.path.split('/')[1]
    elif site == 'own3d':
        sid = o.path.split('/')[2]
    else:
        sid = 0
        
    return {'site': site, 'sid': sid}

def getTwitchStream(user):
    r = http.get_xml('http://api.justin.tv/api/stream/list.xml?channel=%s' % user)
    try:
        viewers = r.xpath('//stream/channel_count/text()')[0]
    except IndexError:
        return False
    if r.xpath('//stream/format/text()')[0] == 'live':
        if viewers:
            return True, viewers
        else:
            return False
    else:
        return False

def getOwnedStream(user):
    h = http.get_xml('http://api.own3d.tv/liveCheck.php?live_id=' + user)
    status = h.xpath('//liveEvent/isLive/text()')[0]
    try:
        viewers = h.xpath('//liveEvent/liveViewers/text()')[0]
    except IndexError:
        return False
    if status == 'true':
        if viewers:
            return True, viewers
        else:
            return False
    else:
        return False

def addStream(url):
    site = parseURL(url)
    print site
    sites = ['twitch', 'own3d']
    if site['site'] not in sites:
        return False
    else:
        if url in r.lrange('stream', 0, -1):
            pass
        else:
            r.rpush('stream', url)

def parseList():
    live = []
    s = r.lrange('stream', 0, -1)
    for stream in s:

        p = parseURL(stream)

        try:
            p['sid']
        except TypeError:
            pass

        if p:
           site = p['site']
           if site == 'twitch':
               try:
                   t, v = getTwitchStream(p['sid'])
                   if t:
                       url = 'http://twitch.tv/' + p['sid']
                       live.append("%s (%s)" % (url, v))
                   else:
                       pass
               except TypeError:
                   pass
           if site == 'own3d':
               try:
                   o, v = getOwnedStream(p['sid'])
                   if o:
                       live.append("%s (%s)" % (stream, v))
                   else:
                       pass
               except TypeError:
                   pass
        else:
             pass
    return live
        

@hook.command('stream')
@hook.command
def streams(inp, say=None):
    c = inp.split(' ')
    if c[0] == 'add':
        addStream(c[1])
        say('Stream added.')
    else:    
        crap = []

        say(" | ".join(parseList()))

if __name__ == "__main__":
    addStream('http://www.own3d.tv/live/184378/Cruzerthebruzer')

    


