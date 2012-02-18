from util import hook, http

twitter_re_status = r"(?i)twitter\.com/#!/(\S+)/status/(\S+)"
linux_re = r"linux"
jerk_re = r"!jerk"

@hook.regex(twitter_re_status)
def twitter_status(match):
	id = match.group(2)
	
	result = http.get_json("http://api.twitter.com/1/statuses/show.json?id=" + id)
	
	at_name = result['user']['screen_name']
	full_name = result['user']['name']
	tweet_text = result['text']
	
	return "\x02@" + at_name + " \x02(" + full_name + ") - " + tweet_text

@hook.regex(linux_re)
def gnu_linux(match, chan=None):
    if chan == "#thesite":
        pass
    else:
        return "I think you meant GNU/Linux."

@hook.regex(jerk_re)
def jerkcrap(match, say=None):
    say("!jerk")
    
