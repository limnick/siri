from util import hook, http
import urllib
import urllib2

@hook.command
def steam(inp, nick='', chan='', say=None):
    inpEncode = urllib.quote(inp)

    try:                                                                                                                                                     
        h = http.get_html("http://steamcalculator.com/id/%s" % inpEncode)                                                                                    
    except urllib2.HTTPError:                                                                                                                                
        return("Hmm it looks like you entered an incorrect name. Be sure that it has no spaces or non ascii characters.") 

    getInfo = h.xpath('//div[@id="leftdetail"]/ul/li/text()')
    getID = getInfo[0]
    getCustomURL = h.xpath('//div[@id="leftdetail"]/ul/li/a/@href')[1]
    getSteamID = getInfo[3]
    getLastOnline = getInfo[4]
    getMemberSince = getInfo[5]

    output = "\x02Username\x0f - %s :: \x02Steam URL\x0f - %s :: \x02Steam ID\x0f - %s :: \x02Last Online\x0f -%s :: \x02Member Since\x0f - %s" % (getID, getCustomURL, getSteamID, getLastOnline, getMemberSince)

    say(output)

@hook.command('sc')
@hook.command
def steamcalc(inp, nick='', chan='', say=None):
    
    '''Usage: '.steamcalc username'. Grab's selected user's steam accounts monetary worth in USD.'''
    
    inpEncode = urllib.quote(inp)
    
    try:
        h = http.get_html("http://steamcalculator.com/id/%s" % inpEncode)
    except urllib2.HTTPError:
        return("Hmm it looks like you entered an incorrect name. Be sure that it has no spaces or non ascii characters.")
    
    try:
        getAmountText = h.xpath('//div[@id="rightdetail"]/text()')[0]
    except IndexError:
        say("That user doesnt exist or something. Fuck off.")
    
    getAmountNum = h.xpath('//div[@id="rightdetail"]/h1/text()')[0]
    #getLastGame = h.xpath('//

    amountSplit = getAmountText.split(' ')
    amountGameNum = int(amountSplit[1])
    
    moneySplit = getAmountNum.split(' ')
    amountMonetary = moneySplit[0]
    
    valueStrip = amountMonetary.strip().lstrip("$")
    value = float(valueStrip)
   
    output = "\x02%s\x0f owns \x02%i\x0f games on Steam. Their account is worth \x02$%.2f\x0f." % (inp, amountGameNum, value)
    
    if amountGameNum >= 125:
        output = output + " <--- jesus fuck quit buying games you neckbeard."

    return(output)
    
    #return "http://steamcalculator.com/id/%s" % inpEncode
