from util import hook, http
from util import http, hook, urlnorm, timesince
from juggernaut import Juggernaut

jug = Juggernaut()

url_re = r'(((https?):\/\/)|www\.)(([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)|localhost|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.(com|net|org|info|biz|gov|name|edu|[a-zA-Z][a-zA-Z]))(:[0-9]+)?((\/|\?)[^"]*[^,;\.:">)])?'

all_re = r'.*'

@hook.regex(all_re)
def log_chat(match, nick='', chan='', say=None, bot=None):
    
    if chan.find("#") == -1:
        return 
    else:
        chan = chan.strip("#")

    if chan == "thesite":
        return

    data = json.dumps({'nick': nick, 'channel': chan, 'message': math.group()})
    jug.publish('links', data)


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
