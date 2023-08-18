import os
import time
from dotenv import load_dotenv
from generate_access_token import get_access_token
from test_fyers import test_fyers_api


def main():
    load_dotenv()
    token_time = float(os.environ.get("TOKEN_DATE"))
    if token_time:
        time_diff = time.time() - token_time
        print("Time Difference is: ", time_diff, "Seconds")
        if time_diff > 21600:
            print("Let's get new access token first.")
            get_access_token()
            test_fyers_api()
        else:
            print("Running tests.")
            test_fyers_api()


if __name__ == "__main__":
    main()
