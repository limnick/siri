from util import hook, http

@hook.command
def haspaid(inp, nick=None):
    if inp == '':
        inp = nick

    thing = " ".join([x for x in http.get("http://www.minecraft.net/haspaid.jsp", user=inp).splitlines() if x])

    if thing == 'true':
        return "%s has bought minecraft." % (inp)
    else:
        return "%s has not bought minecraft." % (inp)
