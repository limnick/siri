import urllib

from util import hook, http
import bitly

spotify_re_http = r"(?i)open\.spotify\.com/(\S+)/(\S+)"
spotify_re_uri = r"(?i)spotify:(\S+):(\S+)"


api = bitly.Api(login='mumphster', apikey='R_fdf99e81477ce574c386c26560112865')

@hook.regex(spotify_re_http)
@hook.regex(spotify_re_uri)
def spotify_link(match):
	j = http.get_json("http://ws.spotify.com/lookup/1/.json?uri=spotify:" + match.group(1) + ":" + match.group(2))
	
	if j.get('error'):
		return
	
	if match.group(1) == "track":
		track = j['track']
		
		out = "Spotify track: \x02" + track['artists'][0]['name'] + " - '" + track['name'] + "'\x02 - " + track['album']['name']
		
	if match.group(1) == "album":
		album = j['album']
		
		out = "Spotify album: \x02" + album['artist'] + "\x02 - " + album['name']
		
	if match.group(1) == "artist":
		
		out = "Spotify artist: " + j['artist']['name']
		
	# to-do: add HTTP link if it comes from a spotify: URI
	return out

@hook.command
def spotify(inp):
    '''.spotify <query> -- returns the first Spotify track result for <query>'''
    inp = urllib.quote(inp)
    j = http.get_json("http://ws.spotify.com/search/1/track.json?q=" + inp)
	
    if j.get('error'):
	    return "error returning search"
		
    if j['info']['num_results'] == 0:
	    return "no results"
	
    track = j['tracks'][0]
    href = track['href']
    href_split = href.split(':')
    spot_type = href_split[1]
    spot_id = href_split[2]
    spot_url = "http://open.spotify.com/%s/%s" % (spot_type, spot_id)

    bitly_url = api.shorten(spot_url) 
    
    dongs = "\x02%s\x0f - \x02%s\x0f - %s\x0f | Spotify URL: %s" % (track['artists'][0]['name'], track['name'], track['album']['name'], bitly_url)
    return dongs

if __name__ == '__main__':
    print spotify('test')
