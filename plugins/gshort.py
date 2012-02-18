import urllib 
import urllib2 
import re
import simplejson


def shorten(url):
  try:
    from re import match
    from urllib2 import urlopen, Request, HTTPError
    from urllib import quote
    from simplejson import loads
  except ImportError, e:
    raise Exception('Required module missing: %s' % e.args[0])
  if not match('http://',url):
    raise Exception('URL must start with "http://"')
  try:
    urlopen(Request('http://goo.gl/api/url','url=%s'%quote(url),{'User-Agent':'toolbar'}))
  except HTTPError, e:
    j = loads(e.read())
    if 'short_url' not in j:
      try:
        from pprint import pformat
        j = pformat(j)
      except ImportError:
        j = j.__dict__
      raise Exception('Didn\'t get a correct-looking response. How\'s it look to you?\n\n%s'%j)
    return j['short_url']
  raise Exception('Unknown eror forming short URL.')

if __name__ == '__main__':
  from sys import argv
  print shorten(argv[1])
