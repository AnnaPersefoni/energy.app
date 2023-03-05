import datetime
from datetime import date


def num_days(date_start, date_end):
    var_start = date_start.replace("/", "")
    var_end = date_end.replace("/", "")

    var_datetime_start = datetime.datetime.strptime(var_start, "%d%m%Y").date()
    var_datetime_end = datetime.datetime.strptime(var_end, "%d%m%Y").date()

    num_days = (var_datetime_end - var_datetime_start).days

    return num_days