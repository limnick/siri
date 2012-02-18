from util import hook, http
import urllib, urllib2


@hook.command
def fanfic(inp, say=None):
    pass

def getfic(inp):
    input = inp.split(" ")[0]
    url = "http://www.fanfiction.net/search.php?type=story&plus_keywords=%s&match=any&minus_keywords=&sort=0&genreid=0&subgenreid=0&characterid=0&subcharacterid=0&words=0&ready=1&categoryid=0" % input
    f = http.get_html(url)
    author = f.xpath('//div[@class="z-list"]/a/text()')[0]
    title = f.xpath('//div[@class="z-list"]/a/b/text()')[0]
    content = f.xpath('//div[@class="z-list"]/div[@class="z-indent z-padtop"]/text()')[0]
    return title + " by " + author + " :: " + content + inp

if __name__ == "__main__":
    print getfic("mlp")
