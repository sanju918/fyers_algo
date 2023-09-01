import json
import sys
from datetime import datetime, timedelta

import pyotp
import requests
import yaml
from dotenv import dotenv_values

from last_thrusday import find_thursday


def status(code, pay_load):
    return {
        "error_code": code,
        "data": pay_load
    }


class Settings:
    def __init__(self, settings_file_path='settings.yml'):
        self.expiry = None
        self.expiry_dates = None
        self.settings_file_path = settings_file_path
        self.settings = None
        self.load_settings()
        secrets = dotenv_values(".env")
        self.app_id = secrets["APP_ID"]
        self.app_type = secrets["APP_TYPE"]
        self.secret_key = secrets["FYERS_SECRET_KEY"]
        self.client_id = f'{self.app_id}-{self.app_type}'
        self.fy_id = secrets['FYERS_ID']
        self.app_id_type = '2'  # 2 denotes web login
        self.totp_key = secrets['TOTP_KEY']
        self.pin = secrets['PIN']

        # API Endpoints
        self.base_url = "https://api-t2.fyers.in/vagator/v2"
        self.base_url_2 = "https://api.fyers.in/api/v2"
        self.login_otp_url = self.base_url + "/send_login_otp"
        self.verify_totp_url = self.base_url + "/verify_otp"
        self.verify_pin_url = self.base_url + '/verify_pin'
        self.token_url = self.base_url_2 + '/token'
        self.validate_auth_code = self.base_url_2 + '/validate-authcode'

    def load_settings(self):
        with open(self.settings_file_path, 'r') as yaml_file:
            settings_data = yaml.safe_load(yaml_file)

        self.settings = settings_data

        # Dynamically destructure the nested settings data
        self._destructure_nested(self.settings, '')

    def _destructure_nested(self, data, prefix):
        for key, value in data.items():
            attr_name = f'{prefix}{key}'
            if isinstance(value, dict):
                self._destructure_nested(value, f'{attr_name}_')
            else:
                setattr(self, attr_name, value)

    def send_login_otp(self):
        try:
            json_ = {"fy_id": self.fy_id, "app_id": self.app_id_type}
            # print("JSON: ", json_)
            res = requests.post(url=self.login_otp_url, json=json_)
            if res.status_code != 200:
                return status(1, res.text)
            result = json.loads(res.text)

            return status(0, result["request_key"])
        except Exception as exp:
            return status(1, exp)

    def verify_totp(self, totp):
        try:
            # print("TRYING")
            request_key = self.send_login_otp()
            # print("RESULT: ", request_key)
            if not request_key["error_code"]:
                print("[Success] Login OTP sent.")
                json_ = {"request_key": request_key["data"], "otp": pyotp.TOTP(totp).now()}
                res = requests.post(url=self.verify_totp_url, json=json_)
                if res.status_code != 200:
                    return status(1, res.text)
                result = json.loads(res.text)
                return status(0, result["request_key"])
            else:
                print(f"[Error] send_login_otp failure - {request_key['data']}")
                sys.exit()
        except Exception as exp:
            return status(1, exp)

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

        expiry = datetime.strptime(expiry_dates[0], "%d-%m-%Y")
        last_thu = str(find_thursday())
        curr_expiry = str(expiry).split(" ")[0]
        
        print("Last Thursday of the month: ", str(last_thu), "Current Expiry", curr_expiry)
        
        if curr_expiry == last_thu:
            print("[Info] This is the last month expiry")
            switcher = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN", 7: "JULY", 8: "AUG", 9: "SEP",
                        10: "OCT", 11: "NOV", 12: "DEC"}
            _date = curr_expiry.split("-")
            _date[1] = switcher[int(_date[1])]
            expiry_date = "-".join(_date)
            print(f"Last Expiry of the Month: {expiry_date}")
            self.expiry = {"year": str(expiry.year - 2000), "month": str(_date[1]), "day": f'{expiry.day:02}'}
        else:
            self.expiry = {"year": str(expiry.year - 2000), "month": str(expiry.month), "day": f'{expiry.day:02}'}

        return self.expiry


