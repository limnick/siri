"weather, thanks to google"

import urllib
from util import hook, http


@hook.command(autohelp=False)
def weather(inp, nick='', server='', reply=None, db=None):
    ".weather <location> [dontsave] -- gets weather data from wunderground"

    loc = inp

    dontsave = loc.endswith(" dontsave")
    if dontsave:
        loc = loc[:-9].strip().lower()

    db.execute("create table if not exists weather(nick primary key, loc)")

    if not loc:  # blank line
        loc = db.execute("select loc from weather where nick=lower(?)",
                            (nick,)).fetchone()
        if not loc:
            return weather.__doc__
        loc = loc[0]
    
    try:
        w = http.get_json('http://api.wundergr'+'ound.com/api/ec53ec'+'c443bc76c4/conditions/q/%s.json'%(urllib.quote(loc))) #chunked to hopefully prevent this key showing up in searches
    except Exception:
        w = None
    
    if not w: #rate limited or api down
        return "Request failed. Try again later"
        
    try:
        info = w['current_observation']
    except KeyError: #city not found
        try: #assemble suggestions
            citynames = []
            for city in w['response']['results'][:10]:
                namestr = city['name']
                if city['state']:
                    namestr += ", %s"%(city['state'])
                elif city['country']:
                    namestr += ", %s"%(city['country'])
                citynames.append(namestr)
            suggestions = "Suggestions: %s"%("; ".join(citynames))
        except KeyError: #no suggestions found
            suggestions = ""
        
        return "Couldn't fetch weather data for '%s', try using a zip or postal code. %s" % (inp, suggestions)
    else: #all gravy
        info['city'] = info['observation_location']['city']
        info['elevation'] = info['observation_location']['elevation']
        reply('%(city)s (elevation: %(elevation)s): %(weather)s, %(temp_f)sF/%(temp_c)sC (Feels Like %(feelslike_f)sF/%(feelslike_c)sC), humidity: %(relative_humidity)s, wind: %(wind_string)s.' % info)

    if inp and not dontsave:
        db.execute("insert or replace into weather(nick, loc) values (?,?)",
                     (nick.lower(), loc))
        db.commit()
