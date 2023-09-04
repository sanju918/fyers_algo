import datetime

# List of holidays
holidays = [
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

weekly_expiry_symbol = {"JAN": "1", "FEB": "2", "MAR": "3", "APR": "4", "MAY": "5", "JUN": "6", "JUL": "7", "AUG": "8",
                 "SEP": "9", "OCT": "O", "NOV": "N", "DEC": "D"}

monthly_expiry_symbols = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

# NSE:NIFTY50-INDEX then it should expire on "THU", if index is NSE:NIFTYBANK-INDEX, it will expire on "WED"
expires = [{"NSE:NIFTY50-INDEX": "THU", "NSE:NIFTYBANK-INDEX": "WED"}]

def is_last_week_of_the_month():
    # should return true if the current date is in the last week
    pass

def check_holiday():
    # check if the current expiry date is falling on any of the date on the holidays list.
    # if current expiry is on the holiday list, then then return the previous day
    pass

def get_expiry_date(index, expires):
    # if current week is not the last week of the month then return expiry in the format YearMonthDate, {YY}{weekley-expiry-format}{dd}, example for 2023-sep-07 it should return 23907,
    # for 2023-Oct--07 it should return 23O07
    # if current week is the last week of the month then return expiry in the format YearMonth, {YY}{montly_expiry_symbols}, example for 2023-Sep-07, it should return 23SEP
    pass