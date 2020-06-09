from datetime import date
from datetime import timedelta

# Find last date from a date_string
# Return last date converted to YYYY-mm-dd or original date_string if no match
# English and French compatible
def find_last_date_from_string(date_string):
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

    today = date.today()
    last_date = None

    if date_string == "Yesterday" or date_string == "Hier":
        last_date = today - timedelta(1)
    elif date_string.lower() in day_offsets:
        offset = (today.weekday() - day_offsets[date_string.lower()]) % 7
        last_date = today - timedelta(days=offset)

    return last_date if last_date is not None else date_string