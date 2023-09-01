import json
from datetime import datetime, timedelta
from dotenv import dotenv_values
from src.last_thrusday import find_thursday


class Settings:
    def __init__(self, path="db.json"):
        self.instruments = None
        secrets = dotenv_values(".env")
        self.app_id = secrets["FYERS_CLIENT_ID"]
        self.app_secret = secrets["FYERS_SECRET_ID"]
        self.access_token = secrets['ACCESS_TOKEN']
        self.old_time_stamp = secrets['TIME_STAMP']

        self.expiry_dates = None
        self.year = None
        self.holidays = None
        self.expiry = None
        self.redirect_url = None
        self.path = path

        self.new_time_stamp = 0
        self.delta_settings = {}
        self.load_settings()

    def load_settings(self):
        with open(self.path, 'r') as json_object:
            settings = json.load(json_object)
        self.delta_settings = settings
        self.redirect_url = settings["variables"]["redirect_url"]
        self.expiry = settings["expiry"]
        self.holidays = settings["holidays"]
        self.year = settings["year"]
        self.instruments = settings["instruments"]
        self.set_expiry()

    def save_settings(self):
        with open(self.path, 'w') as out_file:
            out_file.write(json.dumps(self.delta_settings, indent=4))

    def save_env(self, access_token, time_stamp):
        env_template = f'FYERS_CLIENT_ID={self.app_id}\nFYERS_SECRET_ID={self.app_secret}' \
                       f'\nACCESS_TOKEN={access_token}\nTIME_STAMP={time_stamp}'
        with open('.env', 'w') as out_file:
            out_file.write(env_template)
        print('[INFO]: Saved to environment file')

    def get_weekly_expiry(self):
        holidays = [datetime.strptime(h, "%d-%m-%Y") for h in self.holidays]
        expiry_dates = []
        start_date = datetime.today()
        end_date = datetime(self.year, 12, 31)

        while start_date.weekday() != 3:  # Find the first Thursday of the year
            start_date += timedelta(days=1)

        while start_date <= end_date:
            if start_date not in holidays:
                expiry_dates.append(start_date.strftime("%d-%m-%Y"))
            else:  # If Thursday is a holiday, use the previous trading day as expiry day
                adjusted_expiry_date = start_date - timedelta(days=1)
                while adjusted_expiry_date in holidays:
                    adjusted_expiry_date -= timedelta(days=1)
                expiry_dates.append(adjusted_expiry_date.strftime("%d-%m-%Y"))
            start_date += timedelta(weeks=1)
            if len(expiry_dates) >= 1:
                break

        self.expiry_dates = expiry_dates[0]
        # print("Expiry Date: ", expiry_dates[0])

        return expiry_dates[0]

    def set_expiry(self):
        expiry = self.get_weekly_expiry()
        expiry = datetime.strptime(expiry, "%d-%m-%Y")

        # find last Thursday of the month
        last_thu = str(find_thursday())
        curr_expiry = str(expiry).split(' ')[0]
        print("Last Thursday: ", str(last_thu), "Expiry", curr_expiry)

        if curr_expiry == last_thu:
            print("This is the last month expiry")
            switcher = {1: "JAN", 2:"FEB", 3:"MAR", 4:"APR", 5:"MAY", 6:"JUN", 7:"JULY", 8:"AUG", 9:"SEP", 10:"OCT",
                        11:"NOV", 12:"DEC"}
            _date = curr_expiry.split("-")
            _date[1] = switcher[int(_date[1])]
            expiry_date = "-".join(_date)
            print(f"Last Expiry of the Month: {expiry_date}")
            self.expiry = {"year": str(expiry.year - 2000), "month": str(_date[1]), "day": str(expiry.day)}
        else:
            self.expiry = {"year": str(expiry.year - 2000), "month": str(expiry.month), "day": str(expiry.day)}
        self.delta_settings['expiry'] = self.expiry
        self.save_settings()
        print("[INFO] Current weekly Expiry updated and saved as", self.expiry)


if __name__ == "__main__":
    st = Settings()
    print(st.delta_settings)
    st.get_weekly_expiry()
    print("Current Week Expiry: ", st.expiry_dates)
    st.set_expiry()
