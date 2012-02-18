from util import hook, http
import datetime
from util import timesince

months = { 
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}

full_month = {
    'Jan': 'January',
    'Feb': 'Febuary',
    'Mar': 'March',
    'Apr': 'April',
    'May': 'May',
    'Jun': 'June',
    'Jul': 'July',
    'Aug': 'Augest',
    'Sep': 'September',
    'Oct': 'October',
    'Nov': 'November',
    'Dec': 'December',
}

@hook.command
def legal(inp):
    now = datetime.datetime.now()

    name = inp.replace(' ', '_')
    html = http.get_html('http://rottentomatoes.com/celebrity/%s/' % (name))
    date = html.xpath('//dl[@class="bottom_divider"]/dd/text()')[0]
    #return date

    info = date.split(' ')

    month = info[0]
    birth_day = info[1].strip(",")
    birth_year = info[2]

    birth_month = months[month]

    birthdate = datetime.date(int(birth_year), int(birth_month), int(birth_day))
    age = now.year - int(birth_year)

    if age >= 18:
        return "legal - is %s" % (age)
    else:
        year_18 = int(birth_year) + 18
        birthday_18 = "%s %s %s" % (birth_day, full_month[month], year_18) 
        #return birthday_18

        #return "%s :: %s" % (birth_month, str(day_18))
        return "%s will be 18 in %s" % (inp, timesince.timeuntil(birthdate, now=birthday_18))

    return months[birth_month]
