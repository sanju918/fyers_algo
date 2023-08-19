import os

from fyers_api.Websocket import ws
from fyers_api import fyersModel

from pprint import pprint
from flask import Flask, request
import threading

from dotenv import load_dotenv

load_dotenv('./.env')
app = Flask(__name__)

tokenMapping = {}
ltpDict = {}


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/ltp')
def get_ltp():
    global ltpDict
    print(ltpDict)
    ltp = -1
    instrument = request.args.get('instrument')
    try:
        ltp = ltpDict[instrument]
    except Exception as e:
        print("EXCEPTION occurred while getting ltpDict()")
        print(e)
    return str(ltp)


def on_ticks(ticks):
    global ltpDict
    for tick in ticks:
        ltpDict[tick['symbol']] = tick['ltp']
        pprint(ltpDict)


def start_server():
    print("Inside startServer()")
    app.run(host='0.0.0.0', port=4001)


def test_fyers_api():
    # print("ACCESS TOKEN: ", os.environ.get('ACCESS_TOKEN'))

    # INPUT DATA
    api_key = os.environ.get('FYERS_CLIENT_ID')
    access_token = os.environ.get('ACCESS_TOKEN')

    app_id = api_key
    access_token = access_token
    fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=app_id, log_path="./logs")

    expiry = {
        "year": "23",
        "month": "8",
        "day": "24"
    }

    int_expiry = expiry["year"] + expiry["month"] + expiry["day"]
    strike_list = []
    instrument_list = []

    # NIFTY
    data = {
        "symbols": "NSE:NIFTY50-INDEX"
    }

    ltp = fyers.quotes(data=data)
    if ltp['code'] != 200:
        raise ValueError(ltp['message'])

    a = ltp['d'][0]['v']['lp']
    for i in range(-2, 2):
        strike = (int(a / 100) + i) * 100
        strike_list.append(strike)
        strike_list.append(strike + 50)

    print("STRIKE LIST: ", strike_list)

    # Add Index
    instrument_list.append('NSE:NIFTY50-INDEX')

    # Add CE
    for strike in strike_list:
        ltp_option = "NSE:NIFTY" + str(int_expiry) + str(strike) + "CE"
        instrument_list.append(ltp_option)

    # Add PE
    for strike in strike_list:
        ltp_option = "NSE:NIFTY" + str(int_expiry) + str(strike) + "PE"
        instrument_list.append(ltp_option)

    strike_list = []
    # BANKNIFTY
    data = {
        "symbols": "NSE:NIFTYBANK-INDEX"
    }
    ltp = fyers.quotes(data=data)
    a = ltp['d'][0]['v']['lp']

    for i in range(-2, 2):
        strike = (int(a / 100) + i) * 100
        strike_list.append(strike)

    # Add Index
    instrument_list.append('NSE:NIFTYBANK-INDEX')

    # Add CE
    for strike in strike_list:
        ltp_option = "NSE:BANKNIFTY" + str(int_expiry) + str(strike) + "CE"
        instrument_list.append(ltp_option)

    # Add PE
    for strike in strike_list:
        ltp_option = "NSE:BANKNIFTY" + str(int_expiry) + str(strike) + "PE"
        instrument_list.append(ltp_option)

    instrument_list1 = [
        # "NSE:NIFTY50-INDEX",
        # "NSE:NIFTYBANK-INDEX",
        # "NSE:SBIN-EQ",
        # "MCX:CRUDEOIL23AUGFUT"
    ]

    instrument_list = instrument_list + instrument_list1
    print("BELOW IS THE COMPLETE INSTRUMENT LIST")
    print(instrument_list)
    print("!! Started getltpDict.py !!")
    # END INPUT DATA
    t1 = threading.Thread(target=start_server)
    t1.start()

    access_token_websocket = app_id + ":" + access_token
    fs = ws.FyersSocket(access_token=access_token_websocket, run_background=False, log_path="./logs")
    fs.websocket_data = on_ticks
    fs.subscribe(symbol=instrument_list, data_type="symbolData")
    fs.keep_running()

    t1.join()
    print("websocket started !!")


if __name__ == "__main__":
    load_dotenv('.env')
    # print(os.environ.get("ACCESS_TOKEN"))
    test_fyers_api()