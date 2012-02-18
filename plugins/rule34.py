from util import http, hook
import urllib
from random import choice
from imgur import imgur_get

def search(query):
    term = urllib.quote(query)
    #return term
    try:
        html = http.get_html('http://rule34.paheal.net/post/list/%s/1' % (term))
    except:
        return("The site timed out. It's pretty shitty. Try again in a few seconds.")

    image_link = html.xpath("//div[@id='Imagesmain']/div[@class='thumbblock']/div[@class='rr thumb']/div[@class='rrcontent']/a[2]/@href")
  
    image_link = choice(image_link).split('http://')[1]
    image_safe = urllib.quote(image_link)
    image = "http://" + image_safe
    imgur = imgur_get(image)
    return imgur

@hook.command("ohgod")
@hook.command
def rule34(inp, nick='', say=None):
    return search(inp)

if __name__ == "__main__":
    print search("pokemon")
