import re
import json

import requests
import lxml.html
from util import hook, http


url_re = r'(((https?):\/\/)|www\.)(([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)|localhost|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.(com|net|org|info|biz|gov|name|edu|[a-zA-Z][a-zA-Z]))(:[0-9]+)?((\/|\?)[^"]*[^,;\.:">)])?'

def make_request(inp, lang):
    inputs = inp.split(' ')[0]
    match = re.search(url_re, inputs)
    if match:
        if inputs.find('gist') == -1:
            return make_codepad_request(inp, lang)
        else:
            code = gist_to_text(inputs)
            return make_codepad_request(code, lang)
    else:
        return make_codepad_request(inp, lang)

def make_codepad_request(code, lang):
    url = "http://codepad.org/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-AR; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11',
    }
    
    data = {
        "lang": lang,
        "code": code,
        "run": "True",
        "submit": "Submit"
    }
    r = requests.post(url, data=data, headers=headers, allow_redirects=True)
    html = lxml.html.fromstring(r.content)
    output = html.xpath("//div[@class='highlight']/pre/text()")
   
    if output[4].strip() == "":
        return output[-1].strip('\n')
    else:
        return output[4].strip('\n')

def gist_to_text(gist):
    base = 'http://gist.github.com/'
    gid = gist.split('/')[-1]
    meta = json.loads(requests.get(base + 'api/v1/json/' + str(gid)).content)
    files = meta['gists'][0]['files'][0]
    content = requests.get(base + 'raw/' + gid + '/' + files).content
    return content

@hook.command('c')
def cee(inp):
    return make_request(inp, 'C')

@hook.command('cpp')
def cpp(inp):
    return make_request(inp, 'C++')

@hook.command('d')
def dee(inp):
    return make_request(inp, 'D')

@hook.command('haskell')
def haskell(inp):
    return make_request(inp, 'Haskell')

@hook.command('lua')
def lua(inp):
    return make_request(inp, 'Lua')

@hook.command('ocaml')
def ocaml(inp):
    return make_request(inp, 'Ocaml')

@hook.command('php')
def php(inp):
    return make_request(inp, 'PHP')

@hook.command('perl')
def perl(inp):
    return make_request(inp, 'Perl')

@hook.command('ruby')
def ruby(inp):
    return make_request(inp, 'Ruby')

@hook.command('scheme')
def scheme(inp):
    return make_request(inp, 'Scheme')

@hook.command('tcl')
def tcl(inp):
    return make_request(inp, 'Tcl')

if __name__ == "__main__":
    #d = make_request('print "dongs"', 'Python')
    d = make_request('https://gist.github.com/2004462', 'C')
    print d
    
