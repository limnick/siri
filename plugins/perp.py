# -*- coding: utf-8 -*-

from util import http
import requests
import json
from util import hook
from random import choice

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

class Mugshot(object):
    
    def __init__(self):
        self.list_url = 'http://www.co.washington.ar.us/sheriff/resource/DintakeRoster.asp'
        self.inmate_url = 'http://www.co.washington.ar.us/sheriff/resource/Detainee.asp?bn='

    def url_short(self, url):
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post('https://www.googleapis.com/urlshortener/v1/url', data=json.dumps(payload), headers=headers)
        data = json.loads(r.content)
        url = data['id']
        return url

    def parse_list(self):
        data = http.get_html(self.list_url).xpath('//table/tr/td[@bgcolor]/a/@href')
        ids = [x.split('?')[1].strip('bn=') for x in data]

        return ids

    def get_inmate(self, id_num):
        inmate = {}
        url = self.inmate_url + str(id_num)
        h = http.get_html(url)
        
        try:
            name = h.xpath("//td/font/text()")[0].strip(' ').split(',')

            inmate['first_name'] = name[1].strip(' ')
            inmate['last_name'] = name[0].strip(' ')
            inmate['age'] = h.xpath("//td[text()='Age at Booking:']/following-sibling::td")[0].text
            inmate['race'] = h.xpath("//td[text()='Race:']/following-sibling::td")[0].text
            inmate['sex'] = h.xpath("//td[text()='Sex:']/following-sibling::td")[0].text
            inmate['eyes'] = h.xpath("//td[text()='Eyes:']/following-sibling::td")[0].text
            inmate['hair'] = h.xpath("//td[text()='Hair:']/following-sibling::td")[0].text
            inmate['height'] = h.xpath("//td[text()='Height:']/following-sibling::td")[0].text
            inmate['weight'] = h.xpath("//td[text()='Weight:']/following-sibling::td")[0].text
            inmate['booking_date'] = h.xpath("//td[text()='Booking Date:']/following-sibling::td")[0].text
            inmate['booking_time'] = h.xpath("//td[text()='Booking Time:']/following-sibling::td")[0].text
            inmate['url'] = self.url_short(url)
            
            inmate['charge'] = removeNonAscii(h.xpath("//td/font/text()")[4]).strip()

            r = h.xpath("//td[text()='Race:']/following-sibling::td")[0].text

            if r == 'H':
                race = 'Hispanic'
            elif r == 'A':
                race = 'Asian'
            elif r == 'B':
                race = 'Black'
            else:
                race = 'White'
            
            inmate['race'] = race

            sex = h.xpath("//td[text()='Sex:']/following-sibling::td")[0].text
            if sex == 'F':
                inmate['sex'] = 'Female'
            else:
                inmate['sex'] = 'Male'

            return inmate

        except IndexError:
            return 'inmate does not exist'

@hook.command
def perp(inp, say=None):
    m = Mugshot()
    list = m.parse_list()
    p = m.get_inmate(choice(list))
    
    say('%s, %s - Age: %s - Sex: %s - Race: %s - Height: %s - Weight: %s - Charge: %s - %s' % (p['last_name'], p['first_name'], p['age'], p['sex'], p['race'], p['height'], p['weight'], p['charge'], p['url']))
        
if __name__ == '__main__':
    m = Mugshot()
    inmate = m.get_inmate(4124540)
    print inmate['charge']
