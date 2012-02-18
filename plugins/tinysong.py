from util import hook, http
import urllib

#url = "http://tinysong.com/b/Girl+Talk+Ask+About+Me?format=json"
#i = http.get_json(url)
#print i['Url']
#print i['ArtistName']
#print i['AlbumName']
#print i['SongName']

@hook.command('grooveshark')
@hook.command('searchsong')
@hook.command('ss')
@hook.command
def song(inp, nick='', chan='', say=None):
    inputPlus = urllib.quote_plus(inp)
    #print inputPlus
    url = "http://tinysong.com/b/%s?format=json&key=3490f9a6183cb3f9bb4a054157553142" % (inputPlus)
    #print url
    i = http.get_json(url)
    try: 
        artist = i['ArtistName']
    except TypeError:
        say("No results.. maybe try a more refined query?")
    album = i['AlbumName']
    songName = i['SongName']
    songURL = i['Url']
    
    output = "\x0309Song Name\x0F - %s :: \x0309Artist\x0F - %s :: \x0309Album\x0F - %s :: \x0309Download\x0F - %s" % (songName, artist, album, songURL)
    say(output)

