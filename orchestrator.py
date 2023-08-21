from settings import Settings
import time

from generate_access_token import get_access_token
from test_fyers import test_fyers_api


def main():
    setting_obj = Settings()
    token_time = setting_obj.old_time_stamp

    if token_time:
        time_diff = float(time.time()) - float(token_time)
        print("Time Difference is: ", time_diff, "Seconds")
        if time_diff > 21600:
            print("Let's get new access token first.")
            get_access_token(setting_obj)
            test_fyers_api(setting_obj)
        else:
            print("Running tests.")
            test_fyers_api(setting_obj)


if __name__ == "__main__":
    main()
