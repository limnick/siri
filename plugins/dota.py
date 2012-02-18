from util import hook, http
import cPickle as pickle
import urllib

def xpath_shit(poo):
    xpath = "//div[@id='detailedinfo']/div[@class='windowbg2']/div[@class='content']/table/tr/td[1]/table/tr[%s]/td[2]/text()" % poo
    return xpath

def get_player_info(id):
    url = "http://www.dotalicious-gaming.com/index.php?action=profile;u=%s" % (id)
    html = http.get_html(url)
    played = html.xpath(xpath_shit("4"))[0]
    won = html.xpath(xpath_shit("5"))[0]
    kills = html.xpath(xpath_shit("14"))[0]
    km = html.xpath(xpath_shit("15"))[0]
    deaths = html.xpath(xpath_shit("16"))[0]
    assists = html.xpath(xpath_shit("17"))[0]
    return {"played": played, "won": won, "kills": kills, "km": km, "deaths": deaths, "assists": assists,}

@hook.command('dotes')
@hook.command
def dota(inp, db=None, chan=None, nick=None, say=None):
    
    db.execute("create table if not exists dotes3(id INTEGER, nick)")
    db.commit()

    nick = nick.lower()
    inp = inp.split(" ")
    
    if inp[0] == "reg":
        id = int(inp[1])
        db.execute("insert or replace into dotes3(id, nick) values(?,?)", (id, nick))
        db.commit()
        return("registered with id %s" % (id))

    elif inp[0] == "":
        try:
            id = db.execute("select id from dotes3 where nick=?", (nick.lower(),)).fetchone()[0]
        except:
            return("This user hasnt registered with the bot yet or their ID doesnt exist")
        
        try:
            stats = get_player_info(id)
        except:
            return('That user hasnt registered with the bot.')
        kd = float(stats['kills']) / float(stats['deaths'])
        return("You've played %s games and have won %s. Currently you have %s kills and %s deaths. You've made %s assists and your k/d is %.2f"% (stats['played'], stats['won'], stats['kills'], stats['deaths'], stats['assists'], kd))
    else:
        try:
            id = db.execute("select id from dotes3 where nick=?",
                            (inp[0].lower(),)).fetchone()
        except:
            return("That user hasnt registered with the bot yet or has used a Bad ID")
        
        try:
            stats = get_player_info(id)
        except:
            return('This user hasnt registered their dotalicous ID with the bot.')
        kd = float(stats['kills']) / float(stats['deaths']) 
        return("%s has played %s games and has won %s. Currently that person has %s kills and %s deaths. They've made %s assists and their k/d is %.2f" % (inp[0], stats['played'], stats['won'], stats['kills'], stats['deaths'], stats['assists'], kd))

if __name__ == "__main__":
    print get_player_info("50451")
