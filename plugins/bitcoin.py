from util import http, hook

@hook.command
def bitcoin(inp, say=None, nick='', chan='', conn=None):
    try:
        data = http.get_json("https://mtgox.com/api/0/data/ticker.php")
    except:
        say('mtgox is down or something')

    ticker = data['ticker']
    high = float(ticker['high'])
    low = float(ticker['low'])
    volume = float(ticker['vol'])
    last = float(ticker['last'])
    current = float(ticker['buy'])
    
    say("Current Price: \x0307$%.2f\x0f - High: \x0307$%.2f\x0f - Low: \x0307$%.2f\x0f - Bitcoins Sold Today: %s" % (current, high, low, volume)) 
    #conn.cmd('KICK', [chan, nick, "Suck my dig faggot"]) 
