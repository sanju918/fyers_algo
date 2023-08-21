import datetime
import json
import os

from fyers_api import accessToken
from fyers_api import fyersModel
import webbrowser
from dotenv import load_dotenv
from time import time
import re

FILE_NAME = "db.json"


def get_access_token(settings):
    redirect_uri = "https://www.google.com/"
    client_id = settings['fixed_setting']['FYERS_CLIENT_ID']
    secret_key = settings['fixed_setting']["FYERS_SECRET_ID"]
    grant_type = "authorization_code"
    response_type = "code"
    state = "sample"

    # Connect to the sessionModel object here with the required input parameters
    app_session = accessToken.SessionModel(client_id=client_id, redirect_uri=redirect_uri, response_type=response_type,
                                           state=state, secret_key=secret_key, grant_type=grant_type)

    # Make  a request to generate_authcode object this will return a login url which you need to open in your browser
    # from where you can get the generated auth_code
    generate_token_url = app_session.generate_authcode()
    print(generate_token_url)
    webbrowser.open(generate_token_url, new=1)

    url = input("Enter entire string from web browser URL: ")
    auth_code = re.search(r'auth_code=(.*?)&state', url).group(1)
    app_session.set_token(auth_code)
    response = app_session.generate_token()

    try:
        access_token = response["access_token"]
        # update settings file
        settings["dynamic_settings"]["access_token"] = str(access_token)
        settings["dynamic_settings"]['time_generated'] = float(time())
        print("token: ", access_token)

        fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=client_id, log_path="/")
        fyers.funds()

        with open(FILE_NAME, 'w') as out_file:
            out_file.write(json.dumps(settings))

    except Exception as e:
        print(e, response)


if __name__ == "__main__":
    settings_file = "./db.json"
    with open(settings_file, 'r') as json_file:
        settings_config = json.load(json_file)
    get_access_token(settings_config)
