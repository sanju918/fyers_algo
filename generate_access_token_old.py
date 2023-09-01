from fyers_api import accessToken
from fyers_api import fyersModel
import webbrowser
from time import time
import re

FILE_NAME = "db.json"


def get_access_token(settings_obj):
    redirect_uri = settings_obj.redirect_url
    client_id = settings_obj.app_id
    secret_key = settings_obj.app_secret
    grant_type = "authorization_code"
    response_type = "code"
    state = "sample"

    # Connect to the sessionModel object here with the required input parameters
    app_session = accessToken.SessionModel(client_id=client_id, redirect_uri=redirect_uri, response_type=response_type,
                                           state=state, secret_key=secret_key, grant_type=grant_type)

    # Make  a request to generate_authcode object this will return a login url which you need to open in your browser
    # from where you can get the generated auth_code
    generate_token_url = app_session.generate_authcode()
    print("Generate Token URL: ", generate_token_url)
    webbrowser.open(generate_token_url, new=1)

    url = input("Enter entire string from web browser URL: ")
    auth_code = re.search(r'auth_code=(.*?)&state', url).group(1)
    app_session.set_token(auth_code)
    response = app_session.generate_token()
    if response['code'] == 200:
        access_token = response['access_token']
    else:
        raise ValueError('Unable to generate access_token. Please retry.')

    try:
        # update settings file
        settings_obj.access_token = access_token
        settings_obj.new_time_stamp = time()
        settings_obj.save_env(access_token, time())
        print("Generated new access token: ", access_token)

        fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=client_id, log_path="./logs")
        fyers.funds()

    except Exception as e:
        print("Error: ", e, response)


if __name__ == "__main__":
    from settings import Settings
    obj_settings = Settings()
    get_access_token(obj_settings)
