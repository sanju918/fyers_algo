
import json
import os
import sys

from urllib.parse import urlparse, parse_qs

import pyotp
import requests
import yaml
from dotenv import dotenv_values
from fyers_api import accessToken
from fyers_api import fyersModel


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
                return self.status(1, res.text)
            result = json.loads(res.text)

            return self.status(0, result["request_key"])
        except Exception as exp:
            return self.status(1, exp)

    def verify_totp(self, totp):
        try:
            print("TRYING")
            request_key = self.send_login_otp()
            print("RESULT: ", request_key)
            if not request_key["error_code"]:
                print("[INFO] send_login_otp success")
                json_ = {"request_key": request_key["data"], "otp": pyotp.TOTP(totp).now()}
                res = requests.post(url=self.verify_totp_url, json=json_)
                if res.status_code != 200:
                    return self.status(1, res.text)
                result = json.loads(res.text)
                return self.status(0, result["request_key"])
            else:
                print(f"[ERROR] send_login_otp failure - {request_key['data']}")
                sys.exit()
        except Exception as exp:
            return self.status(1, exp)

    def status(self, code, pay_load):
        return {
            "error_code": code,
            "data": pay_load
        }


def main():
    conf = Settings()
    session = accessToken.SessionModel(
        client_id=conf.client_id,
        secret_key=conf.secret_key,
        response_type='code',
        grant_type='authorization_code',
        redirect_uri=getattr(conf, 'redirect_url')
    )

    # print(conf.client_id, conf.secret_key, conf.redirect_url)
    url_to_activate = session.generate_authcode()
    print(f'URL to activate APP:  {url_to_activate}')

    verify_totp_result = None

    for _ in range(1, 3):
        verify_totp_result = conf.verify_totp(conf.totp_key)
        print("VERIFY: ", verify_totp_result)
        if verify_totp_result['error_code']:
            print('[ERROR] Verify TOTP failed.', verify_totp_result['data'])
        else:
            print('[SUCCESS] TOTP Successfully verified.', verify_totp_result['data'])
            break

    req_key = verify_totp_result['data']

    ses = requests.Session()
    payload_pin = {
        "request_key": f'{req_key}',
        "identity_type": "pin",
        "identifier": f"{conf.pin}",
        "recaptcha_token": ""
    }

    req_url = 'https://api-t2.fyers.in/vagator/v2/verify_pin'
    res_pin = ses.post(url=req_url, json=payload_pin).json()
    print(res_pin['data'])
    ses.headers.update({'authorization': f"Bearer {res_pin['data']['access_token']}"})

    auth_param = {"fyers_id": conf.fy_id, "app_id": conf.app_id, "redirect_uri": getattr(conf, 'redirect_url', None),
                  "appType": conf.app_type, "code_challenge": "", "state": "None",
                  "scope": "", "nonce": "", "response_type": "code", "create_cookie": True}
    print("AUTH PARAMS: ", auth_param)
    authres = ses.post('https://api.fyers.in/api/v2/token', json=auth_param).json()
    print(authres)
    url = authres['Url']
    print(url)
    parsed = urlparse(url)
    auth_code = parse_qs(parsed.query)['auth_code'][0]

    session.set_token(auth_code)
    response = session.generate_token()
    conf.access_token = response['access_token']
    print(f"[INFO] ACCESS TOKEN: {conf.access_token}")

    fyers_model = fyersModel.FyersModel(
        client_id=conf.client_id,
        token=conf.access_token,
        log_path=os.getcwd()
    )

    print(f'[INFO] {fyers_model.get_profile()}')


if __name__ == '__main__':
    main()
