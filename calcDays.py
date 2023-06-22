import datetime
from datetime import date


def num_days(date_start, date_end):
    print(date_start)
    var_start = date_start.replace("-", "")
    var_end = date_end.replace("-", "")

    var_datetime_start = datetime.datetime.strptime(var_start, "%Y%m%d").date()
    var_datetime_end = datetime.datetime.strptime(var_end, "%Y%m%d").date()

    num_days = (var_datetime_end - var_datetime_start).days

    return num_days