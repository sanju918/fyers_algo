import os

from fyers_api import accessToken
from fyers_api import fyersModel
import webbrowser
# from dotenv import load_dotenv
from time import time


def get_access_token():
    # load_dotenv()

    redirect_uri = "https://www.google.com/"
    client_id = os.environ.get('FYERS_CLIENT_ID')
    secret_key = os.environ.get('FYERS_SECRET_ID')
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

    auth_code = input("Enter Auth Code: ")
    app_session.set_token(auth_code)
    response = app_session.generate_token()

    try:
        access_token = response["access_token"]
        print("token: ", access_token)
        fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=client_id, log_path="/")
        fyers.funds()

        environment_variables = f'FYERS_CLIENT_ID={client_id}\nFYERS_SECRET_ID={secret_key}\n' \
                                f'ACCESS_TOKEN={access_token}\nTOKEN_DATE={time()}'
        os.environ.setdefault("ACCESS_TOKEN", access_token)

        with open(".env", 'w') as env_file:
            env_file.write(environment_variables)

    except Exception as e:
        print(e, response)


if __name__ == "__main__":
    get_access_token()
