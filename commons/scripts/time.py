from django.utils.timezone import now
import datetime


def time_diff_in_hours(to_time: datetime.datetime, from_time: datetime.datetime) -> int:
    """
    Returns time difference of datetime.datetime format times in hours.
    """

    delta = abs(to_time - from_time)
    return int(delta.days * 24 + delta.seconds / 3600.0)


def is_current_week_in_range(start_week: int, end_week: int) -> bool:
    """
    Checks if current week number is in the range of start week and end week.

    returns: A boolean about today is in week range or not.
    """

    current_week = datetime.date.today().isocalendar()[1]
    if start_week > end_week:
        not (current_week in range(end_week, start_week + 1))
    else:
        return current_week in range(start_week, end_week + 1)
