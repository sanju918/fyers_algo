# importing the requests library
import requests
import time


def getLTP(instrument):
    url = "http://localhost:4001/ltp?instrument=" + instrument
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    data = resp.json()
    return data


def main():
    while True:
        k = getLTP('NSE:SBIN-EQ')
        print(" K = ", k)
        time.sleep(2)


main()
