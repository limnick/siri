from util import hook, http


@hook.command
def ghetto(inp, say=None):
    wtf = http.get_html("http://ghettoradio.us/wtf.php")
    nowplaying = wtf.xpath('//text()')[0]
    say(nowplaying)
