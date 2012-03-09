import urlparse
import http
import urllib2

class VideoParse(object):
    def __init__(self, video):
        self.video = video
        host = video.split('//')[1].split('/')[0]
        if host.find('youtube') == -1:
            if host.find('vimeo') == -1:
                return None
            else:
                id = video.split('/')[3]
                self.title, self.thumbnail, self.host, self.id = self.vimeo_parse(id)
        else:
            parse_data = urlparse.urlparse(video)
            query = urlparse.parse_qs(parse_data.query)
            id = query["v"][0]
            self.title, self.thumbnail, self.host, self.id = self.youtube_parse(id)

    def vimeo_parse(self, id):
        self.id = id
        json = http.get_json("http://vimeo.com/api/v2/video/%s.json" % id)
        title = json[0]["title"]
        thumbnail = json[0]["thumbnail_large"]
        host = "vimeo"
        id = id

        return title, thumbnail, host, id

    def youtube_parse(self, id): 
        self.id = id
        json = http.get_json("http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=jsonc" % id)
        j = json['data']
        host = "youtube"
        thumbnail = "http://img.youtube.com/vi/%s/2.jpg" % id
        title = j['title']

        return title, thumbnail, host, id

class WebsiteParse(object):
    def __init__(self, url):
        self.url = url
        html = http.get_html(url)
        title_crap = html.xpath("//title/text()")[0]
        if title_crap == '':
            self.title = "No Title Found"
        else: 
            self.title = title_crap

class SiteParse(object):
    def __init__(self, url):
        self.url = url
        
        host = url.split('//')[1].split('/')[0]
        print host
        
        if host.find('youtube') != -1:
            self.category = "video"
            return

        headers = urllib2.urlopen(url).info()
        content = headers['Content-Type'].split(' ')[0].split('/')[0]
        
        if content == "image":
            self.category = "image"
            return

        elif content == "audio":
            self.category ="music"
            return

        else:
            self.category = "website"
            return

if __name__ == "__main__":
    youtube = "http://www.youtube.com/watch?v=tkE-cCJ--Cc&feature=feedrec_grec_index"
    site = "http://google.com/"
    poop = SiteParse(youtube)
    ypoop = SiteParse(site)
    print poop.category
    print ypoop.category
