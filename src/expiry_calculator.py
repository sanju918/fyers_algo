import calendar
from datetime import datetime, timedelta


def get_last_day_of_month(cal, year, month, day_name, day_number):
    """
    For example, get_thursday(cal, 2017,8,0) returns (2017,8,3)
    because the first thursday of August 2017 is 2017-08-03
    """
    switcher = {
        'MON': calendar.MONDAY, 'TUE': calendar.TUESDAY, 'WED': calendar.WEDNESDAY, 'THU': calendar.THURSDAY,
        "FRI": calendar.FRIDAY, 'SAT': calendar.SATURDAY, 'SUN': calendar.SUNDAY
    }
    monthcal = cal.monthdatescalendar(year, month)
    selected_thursday = [day for week in monthcal for day in week if \
                         day.weekday() == switcher[day_name] and \
                         day.month == month][day_number]
    return selected_thursday


def find_monthly_expiry(day_name, date, holidays):
    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    year = date.year
    month = date.month
    selected_day = get_last_day_of_month(cal, year, month, day_name, -1).strftime("%Y-%m-%d")

    if selected_day not in holidays:
        return selected_day
    else:
        # Find the nearest previous non-holiday date
        while selected_day in holidays:
            selected_day -= timedelta(days=1)
        return selected_day


def get_weekly_expiry(day_str, dt, holidays):
    switcher = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    if day_str in switcher:
        expiry_index = switcher.index(day_str)
    else:
        raise ValueError(f'[Err] Invalid expiry day: {day_str}')
    # Get the current date
    # current_date = datetime.today()
    current_date = dt

    # Find the day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
    current_day_of_week = current_date.weekday()

    # Calculate the number of days to Thursday (assuming Thursday is 3)
    days_until = (expiry_index - current_day_of_week) % 7

    # Calculate the Thursday date by adding the days_until_thursday to the current date
    exp_date = current_date + timedelta(days=days_until)

    # Find the nearest previous non-holiday date
    while exp_date in holidays:
        exp_date -= timedelta(days=1)

    # Format the Thursday date as a string in the desired format
    exp_date_formatted = exp_date.strftime("%Y-%m-%d")

    return exp_date_formatted


def get_expiry(day: str, holiday_list: list, for_date: datetime = datetime.today()):
    """
    :param day: 'WED', 'THU'
    :param holiday_list: ["2023-01-26", "2023-03-07",]
    :param for_date: datetime.today()
    :return: for weekly expiry 23D07, for monthly 23DEC
    """
    # Convert holiday strings to datetime.date objects
    holidays = [datetime.strptime(date_str, "%d-%m-%Y").date() for date_str in holiday_list]
    weekly_expiry = datetime.strptime(get_weekly_expiry(day, for_date, holidays), "%Y-%m-%d")
    monthly_expiry = datetime.strptime(find_monthly_expiry(day, for_date, holidays), "%Y-%m-%d")

    # print("Weekly Expiry: ", weekly_expiry, "Monthly Expiry: ", monthly_expiry)

    if weekly_expiry == monthly_expiry:
        return monthly_expiry.strftime("%y%b").upper()
    else:
        month_matcher = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'O', 'N', 'D']
        month = month_matcher[int(weekly_expiry.month) - 1]

        return weekly_expiry.strftime(f"%y{month}%d")


if __name__ == "__main__":
    holidays_str = [
        "2023-01-26",
        "2023-03-07",
        "2023-03-30",
        "2023-04-04",
        "2023-04-07",
        "2023-04-14",
        "2023-05-01",
        "2023-06-28",
        "2023-08-15",
        "2023-09-19",
        "2023-10-02",
        "2023-10-24",
        "2023-11-14",
        "2023-11-27",
        "2023-12-25"
    ]

    # dt = datetime.today()
    dt = datetime(2023, 12, 25)
    days = "THU"
    expiry = get_expiry(days, holidays_str, dt)
    print(expiry)
