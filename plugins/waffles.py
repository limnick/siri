from util import http, hook
from imgur import imgur_get 

@hook.command
def waffles(inp):
    link = http.get_html('http://randomwaffle.gbs.fm')
    image = link.xpath('//img/@src')[0]
    image_url = "http://randomwaffle.gbs.fm/%s" % (image)
    imgur_link = imgur_get(image_url)
    return imgur_link 

