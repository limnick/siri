import re
from os import listdir
from random import choice
from util import hook, http

@hook.command
def jiggle(inp, nick='', chan='', say=None):
	dir = "/usr/local/lsws/MUSIC/html/jiggle/"
	tits = "http://herearemytits.com/j.php?i=%s" % (random_file(dir))
	say("plugin currently being re-writtien.")
