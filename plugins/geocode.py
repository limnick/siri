from geopy import geocoders
from util import hook, http



g = geocoders.Google('ABQIAAAABO-w31VIffxjpgdCZcxSyRSyIgII6-8lsWmH0PnQTlXyRwLzcxSB8zgOu_4dlTfKNmUSWsfiUM0G')

@hook.command
def geocode(inp, nick='', chan='', say=None):
    place, (lat, lng) = g.geocode(inp)
    return "%s: %.5f, %.5f" % (place, lat, lng)

