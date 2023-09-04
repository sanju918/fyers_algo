import json
import sys

import pyotp
import requests
import yaml
from dotenv import dotenv_values

from expiry_calculator import get_expiry


def status(code, pay_load):
    return {
        "error_code": code,
        "data": pay_load
    }


class Settings:
    def __init__(self, settings_file_path='settings.yml'):
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
            request_key = self.send_login_otp()
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

    def get_weekly_expiry(self, index):

        # find day 'THU' or 'WED' based on index
        expiry_day = None
        for exp in self.expires:
            # print(f"Given INDEX: {index}, Setting EXPIRY INDEX: {exp['index']}")
            if index == exp['index']:
                expiry_day = exp['expiry']
                # print("Expiry Day: ", expiry_day)
        if expiry_day is None:
            raise ValueError(f'[Err] Invalid index {index} provided to calculate expiry.')

        expiry = get_expiry(expiry_day, self.holidays)
        # print("Expiry: ", expiry)
        return expiry