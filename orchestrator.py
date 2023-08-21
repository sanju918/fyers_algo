from settings import Settings
import time

from generate_access_token import get_access_token
from fyers_server import test_fyers_api


def time_converter(seconds):
    days = int(seconds / 86400)
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d Days, %02d:%02d:%02d (hh:mm:ss)" % (days, hour, minutes, seconds)


def main():
    setting_obj = Settings()
    token_time = setting_obj.old_time_stamp
    # print("Last token time: ", token_time)

    if token_time:
        time_diff = float(time.time()) - float(token_time)
        # print("Time Diff: ", time_diff)
        # print(time_converter(time_diff))
        print("[INFO] Last token generated before: ", time_converter(time_diff))
        # return
        if time_diff > 21600:
            print("[INFO]Token is more than 6 hr old, let's get new access token first.")
            get_access_token(setting_obj)
            test_fyers_api(setting_obj)
        else:
            print("[INFO] Starting Live Server.")
            test_fyers_api(setting_obj)


if __name__ == "__main__":
    main()
