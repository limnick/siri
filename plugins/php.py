from util import http, hook
import urllib

def php(code):
    '''executes php code'''
    code = urllib.quote(code)
    
    try:
        html = http.get_html('http://writecodeonline.com/php/?code=%s' % code)
    except:
        return "php sucks. site is down or something. what a shock"

    output = html.xpath('//div[@id="code-output"]/text()')[0]
    return output

@hook.command('php')
def fuckphp(inp, nick=None, say=None):
    '''.php <code> - executes php code'''
    return php(inp)

if __name__ == '__main__':
    print php("echo 'hello world';")
