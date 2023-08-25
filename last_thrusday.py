import calendar
import datetime


def get_thursday(cal, year, month, thursday_number):
    """
    For example, get_thursday(cal, 2017,8,0) returns (2017,8,3)
    because the first thursday of August 2017 is 2017-08-03
    """
    monthcal = cal.monthdatescalendar(year, month)
    selected_thursday = [day for week in monthcal for day in week if \
                         day.weekday() == calendar.THURSDAY and \
                         day.month == month][thursday_number]
    return selected_thursday


def find_thursday():
    """
    Show the use of get_thursday()
    """
    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    date = get_thursday(cal, year, month, -1)  # -1 because we want the last Thursday
    # date = "-".join(str(date).split("-")[::-1])
    # print(date)  # date: 31-08-2023
    return date


if __name__ == "__main__":
    find_thursday()
