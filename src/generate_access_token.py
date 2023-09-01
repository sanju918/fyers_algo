import os
from urllib.parse import urlparse, parse_qs

import requests
from fyers_api import accessToken, fyersModel

from settings import Settings


def generate_access_token():
    conf = Settings()
    expiry = conf.get_weekly_expiry()
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
        # print("VERIFY: ", verify_totp_result)
        if verify_totp_result['error_code']:
            print('[ERROR] Verify TOTP failed.', verify_totp_result['data'])
        else:
            # print('[SUCCESS] TOTP Successfully verified.', verify_totp_result['data'])
            print('[SUCCESS] TOTP Successfully verified.')
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

    ses.headers.update({'authorization': f"Bearer {res_pin['data']['access_token']}"})

    auth_param = {"fyers_id": conf.fy_id, "app_id": conf.app_id, "redirect_uri": getattr(conf, 'redirect_url', None),
                  "appType": conf.app_type, "code_challenge": "", "state": "None",
                  "scope": "", "nonce": "", "response_type": "code", "create_cookie": True}
    # print("AUTH PARAMS: ", auth_param)
    authres = ses.post('https://api.fyers.in/api/v2/token', json=auth_param).json()
    # print(authres)
    url = authres['Url']
    # print(url)
    parsed = urlparse(url)
    auth_code = parse_qs(parsed.query)['auth_code'][0]

    session.set_token(auth_code)
    response = session.generate_token()
    access_token = response['access_token']
    # print(f"[INFO] ACCESS TOKEN: {access_token}")

    fyers_model = fyersModel.FyersModel(
        client_id=conf.client_id,
        token=access_token,
        log_path=os.getcwd()
    )

    profile_data = fyers_model.get_profile()

    if profile_data['code'] != 200:
        print("[Error] Unable to get profile information at this moment.")
    else:
        print(f'[INFO] Profile data: {profile_data}')

    instrument_list = getattr(conf, 'instruments', [])

    return access_token, conf


if __name__ == '__main__':
    generate_access_token()
