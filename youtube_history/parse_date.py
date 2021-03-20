import datetime
from datetime import date
from datetime import timedelta

import re

# Find last date from a date_string
# Return last date converted to YYYY-mm-dd or original date_string if no match
# English and French compatible
def find_last_date_from_string(date_string):

    # List of weekdays offset in English and French
    day_offsets = {
        "monday": 0,
        "lundi": 0,
        "tuesday": 1,
        "mardi": 0,
        "wednesday": 2,
        "mercredi": 2,
        "thursday": 3,
        "jeudi": 3,
        "friday": 4,
        "vendredi": 4,
        "saturday": 5,
        "samedi": 5,
        "sunday": 6,
        "dimanche": 6,
    }

    # List of months values in English and French
    months_number = {
        "january": "01",
        "janvier": "01",
        "february": "02",
        "février": "02",
        "march": "03",
        "mars": "03",
        "april": "04",
        "avril": "04",
        "may": "05",
        "mai": "05",
        "june": "06",
        "juin": "06",
        "july": "07",
        "juillet": "07",
        "august": "08",
        "aout": "08",
        "september": "09",
        "septembre": "09",
        "october": "10",
        "octobre": "10",
        "november": "11",
        "novembre": "11",
        "december": "12",
        "décembre": "12"
    }

    today = date.today()
    last_date = None

    if date_string == "Today" or date_string == "Aujourd'hui":
        last_date = today
    if date_string == "Yesterday" or date_string == "Hier":
        last_date = today - timedelta(1)
    elif date_string.lower() in day_offsets:
        offset = (today.weekday() - day_offsets[date_string.lower()]) % 7
        last_date = today - timedelta(days=offset)
    else:
        # Regex to find a matching pattern with an English or French date
        date_regex = "(\d{1,2} [a-zA-Z]+)|([a-zA-Z]+ \d{1,2})"
        result = re.match(date_regex, date_string)

        # If a matching pattern is found, we convert the date string to a YYYY-mm-dd
        if result:
            now = datetime.datetime.now()
            day_weekday = result.group().split(" ")

            if day_weekday[0].lower() in months_number or day_weekday[1].lower() in months_number:
                # English match
                if day_weekday[0].lower() in months_number:
                    if len(day_weekday[1]) == 1:
                        day_weekday[1] = "0" + str(day_weekday[1])
                    last_date = str(now.year) + "-" + str(months_number[day_weekday[0].lower()]) + "-" + str(day_weekday[1])
                # French match
                else: 
                    if len(day_weekday[0]) == 1:
                        day_weekday[0] = "0" + str(day_weekday[0])
                    last_date = str(now.year) + "-" + str(months_number[day_weekday[1].lower()]) + "-" + str(day_weekday[0])

    return last_date if last_date is not None else date_string