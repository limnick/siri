from util import hook, http



@hook.command
def log(inp, nick='', chan='', say=None):
    
    chan = chan.strip("#")
    base = "http://catteproject.troutslap.me/%s/" % chan
    
    if inp == 'youtube':
        output = base + "youtube"
        say(output)
    
    if inp == 'images':
        output = base + "pics" + " \x03/!\NSFW/!\ \x0f"
        say(output)
    
    if inp == 'music':
        output = base + "music"
        say(output)
    
    if inp == '':
        output = base + "links" + " \x03/!\NSFW/!\ \x0f"
        say(output)
        

