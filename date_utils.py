from datetime import datetime, date


def days_between(date1, date2):
    delta = date2 - date1
    return abs(delta.days)


def is_weekend(d):
    return d.weekday() >= 5


def format_date(d, fmt='%Y-%m-%d'):
    return d.strftime(fmt)


def start_of_month(d):
    return d.replace(day=1)


def age_in_years(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
