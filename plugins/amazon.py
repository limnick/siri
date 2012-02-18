import urllib
from util import http, hook
import bitly
from amazonproduct import API
import urllib2

class tinyurl:
        
    API_CREATE_URI = "http://tinyurl.com/api-create.php?url=%s"
        
    def __init__(self, url):
        self.url = url
        
    def create(self):
        encoded_url = urllib.urlencode({'url':self.url})[4:]
        new_url = tinyurl.API_CREATE_URI % (encoded_url)
        tinyurl_request = urllib2.Request(new_url)
        tinyurl_handle = urllib2.urlopen(tinyurl_request)
        return tinyurl_handle.read()


AWS_KEY = 'AKIAIHJVUUXJBL5CHPMA'
SECRET_KEY = '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'
 
api = API(AWS_KEY, SECRET_KEY, "us")

def asearch(keyword):
    node = api.item_search('All', Keywords=keyword)
    title = node.Items.Item[0].ItemAttributes.Title
    url = node.Items.Item[0].DetailPageURL
    #short_url = tiny_url(url)
    return title, url 

@hook.command('amazon')
@hook.command
def amazonsearch(inp, nick='', chan='', say=None):
    title, url = asearch(inp)
    a = tinyurl(url)
    return "%s :: \x02%s\x0f" % (title, a.create())

if __name__ == '__main__':
    title, url = asearch('1215n')
    print title
    a = tinyurl(url) 
    print a.create()
