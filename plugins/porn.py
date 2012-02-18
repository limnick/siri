from util import hook, http
import re
import urllib

@hook.command
def redtube(inp, nick='', chan='', say=None):
    search = urllib.quote_plus(inp)
    searchURL = "http://redtube.com/?search=%s" % (search)
    getSearch = http.get_html(searchURL)
    videoTitle = getSearch.xpath('/html/body/div/div/div[3]/ul/li/div[2]/h2/a/')[0]
    #videoUrl = getSearch.xpath('//div[@class="video"]/a/href/text()')[0]
    #final = "%s :: %s" % (videoTitle, videoUrl)
    say(videoTitle)
