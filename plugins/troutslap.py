from util import hook, http
import slumber #thanks dittoed!
from util import http, hook, urlnorm, timesince

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

    if 'trout_api_key' not in bot.config or \
        'trout_api_username' not in bot.config or \
        'trout_api_botname' not in bot.config:
        return
    
    username = str(bot.config['trout_api_username'])
    api_key = str(bot.config['trout_api_key'])
    bot_name = str(bot.config['trout_api_botname'])

    api = slumber.API("http://troutslap.me/api/v1/")
    

    try:
        api.log.post({"nick": nick, "channel": chan, "message": match.group()}, username=username, api_key=api_key)
    except Exception, e:
        print e.content

@hook.regex(url_re)
def submit_url(match, nick='', chan='', bot=None):
   
    if chan.find("#") == -1:
        return
    else:
        chan = chan.strip('#')
    
    if chan == "thesite":
        return

    url = urlnorm.normalize(match.group().encode('utf-8'))
    url = url.decode('utf-8')
    
    if 'trout_api_key' not in bot.config or \
       'trout_api_username' not in bot.config or \
       'trout_api_botname' not in bot.config:
        return
    
    username = str(bot.config['trout_api_username'])
    api_key = str(bot.config['trout_api_key'])
    bot_name = str(bot.config['trout_api_botname'])

    api = slumber.API("http://troutslap.me/api/v1/")
    api.url.post({"url": url, "nick": nick, "channel": chan}, username=username, api_key=api_key)
