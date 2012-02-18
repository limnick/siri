import pylast
from util import hook, http
import urllib
import bitly

bitly_api = bitly.Api(login='mumphster', apikey='R_fdf99e81477ce574c386c26560112865')

#lastFM Lookup - http://last.fm

@hook.command
def lastfm(inp, reply=None, say=None, nick=''):
   API_KEY = "30cabd8b57c765a42f78e8f5d329fdc0"
   API_SECRET = "0ab2d0a46763e71d1ed8877b4ea209cf"
   username = "elgruntox"
   password_hash = pylast.md5("justpurple")
   network = pylast.get_lastfm_network(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)
   try:   
      if inp == '':
         user = network.get_user(nick)
      else: 
         user = network.get_user(inp)
         nick = inp
   except WSError:
      say("This user doesn't exist.")
   try:
      tracks = user.get_recent_tracks()
   except pylast.WSError:
       if inp == '':
          return("It seems like your current nickname does not have a lastFM account. Try '.lastfm username' instead.")  
       else: 
          return("The user '%s' does not exist. Maybe you misspelled it?" % inp)
   recent = tracks[0][0]
   artist = recent.get_artist().get_name()
   title = recent.get_title()
   url = recent.get_url()
   bitlyURL = bitly_api.shorten(url) 

   finalise = "\x02%s\x0F's last track - \x02%s\x0f :: Artist - \x02%s\x0f :: Link to Song - \x02%s\x0F" % (nick, title, artist, bitlyURL)
   say(finalise)


   
