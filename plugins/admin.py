from util import hook, http

@hook.command(adminonly=True)
def admintest(inp, nick='', chan='', say=None):
    say("waddup %s" % nick)

@hook.command(adminonly=True)
def channeljoin(inp, conn=None, nick='', chan='', say=None):
   conn.join(inp)
   say("Joining %s" % inp)

@hook.command(adminonly=True)
def kickuser(inp, conn=None, nick='', chan='', say=None):
    conn.cmd('KICK', [chan, inp])
    say("%s kicked" % inp)

@hook.command(adminonly=True)
def changenick(inp, input=None, bot=None):
    input.set_nick(inp)

@hook.command(adminonly=True)
def leavechan(inp, nick='', say=None, conn=None):
    conn.cmd('PART', [inp])
    say("Leaving %s" % chan)


