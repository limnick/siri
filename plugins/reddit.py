from util import http, hook
import re
import urllib

@hook.command
def reddit(inp, nick=None, say=''):
    query = urllib.quote_plus(inp)

    splitQuery = query.split(" ")
    if re.match("r/", splitQuery[0]):
        try:
            json = http.get_json("http://reddit.com/%s/search.json?q=%s" % (splitQuery[0], query))
        except:
            return "REDDIT IS DOOOOOWN"

    else:
        try:
            json = http.get_json("http://reddit.com/search.json?q=%s" % (query))
        except:
            return "REDDIT IS DOOOOOWN"

    try:
        data = json['data']['children'][0]['data']
    except:
        return "Search returned nothing broseph."

    id = data['id'] # id to use with reddit url shortener 
    is_self = data['is_self'] # is this a self post - returns true or false
    num_comments = data['num_comments'] 
    adult = data['over_18'] # returns True or False - if submission is nsfw
    score = data['score']
    subreddit = data['subreddit']
    title = data['title']
    url = data['url'] # returns submissions full url
    
    if adult == True:
        porn = "[NSFW]"
    else:
        porn = ''
    
    return "%s :: /r/%s :: http://redd.it/%s %s" % (title, subreddit, id, porn)
