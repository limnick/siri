from util import http, hook
import re
import bitly


fb_re = r'\/([0-9]*_){5}.*\.(jpg|jpeg|gif)'

api = bitly.Api(login='mumphster', apikey='R_fdf99e81477ce574c386c26560112865')

@hook.regex(fb_re)
def fb_info(match):
    id = match.group().split('_')[2]
    info = http.get_json('http://graph.facebook.com/%s' % id)

    name = info['name']
    link = api.shorten(info['link'])
    
    if info['gender'] == "female":
        return ("A girl posted that! %s - %s" % (name, link))
    else:
        return ("Some gay guy posted that. %s - %s" % (name, link))


@hook.command()
def testcat(inp):
    cat = http.get_html('http://api.cattes.us/catte/')
    return cat.xpath('//img/@src')[0]
