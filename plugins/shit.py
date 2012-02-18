from util import hook, http


@hook.regex(r'^(?i)Wrex(.$|$)')
def wrex(inp, unused=None):
    return 'Shepard.'

@hook.regex(r'^(?i)Shepard(.$|$)')
def shepard(inp, unused=None):
    return 'Wrex.'

