from fyers_api.Websocket import ws
from fyers_api import fyersModel

from pprint import pprint
from flask import Flask, request
import threading

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


def get_opt_instruments_list(fyers, symbol: str, expiry_str):
    strike_list = []
    instrument_list = []
    data = {"symbols": symbol}

    ltp = fyers.quotes(data=data)
    if ltp['code'] == 200:
        print("[Info] Last Trading Price: ", ltp['d'][0]['v'])

    strike = 0

    if ltp['code'] == 200 and ltp['d'][0]['s'] == 'ok':
        strike = ltp['d'][0]['v']['lp']
    else:
        raise ValueError(f"[Err] {ltp['d'][0]['v']['code']} {ltp['d'][0]['v']['errmsg']}")

    if ltp['code'] == '500':
        raise ConnectionError(ltp['data'])
    elif ltp['code'] == -15:
        raise ValueError(ltp['message'])
    elif ltp['code'] != 200:
        raise ValueError(ltp)

    if strike > 0:
        for i in range(-2, 2):
            strike = (int(strike / 100) + i) * 100
            strike_list.append(strike)
            if symbol == 'NSE:NIFTY50-INDEX':
                strike_list.append(strike + 50)

    print("[Info] STRIKE LIST: ", strike_list)

    # NSE:NIFTY2390719400CE

    if strike_list:
        mapper = {'NSE:NIFTY50-INDEX': "NSE:NIFTY", "NSE:NIFTYBANK-INDEX": 'NSE:BANKNIFTY'}
        for strike in strike_list:
            ltp_option = mapper[symbol] + expiry_str + str(strike)
            instrument_list.append(ltp_option + "CE")
            instrument_list.append(ltp_option + "PE")

        return instrument_list

    else:
        raise ValueError("[Error] Can't determine instrument list. Please check correct expiry.")


def run_server(access_token: str, conf: object):
    app_id = getattr(conf, 'app_id', '')
    access_token = access_token
    fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=app_id, log_path="./logs")

    # Add Indexes 'NSE:NIFTYBANK-INDEX', 'NSE:NIFTY50-INDEX',
    index_list = ['NSE:NIFTY50-INDEX', 'NSE:NIFTYBANK-INDEX']
    instrument_list = []

    for index in index_list:
        expiry = conf.get_weekly_expiry(index)
        print(f"[Info] Expiry for {index} :", expiry)

        temp_inst_list = get_opt_instruments_list(fyers, index, expiry)
        instrument_list.extend(temp_inst_list)

    instrument_list.extend(getattr(conf, 'instruments', None))
    instrument_list.extend(index_list)

    print("[Info] BELOW IS THE COMPLETE INSTRUMENT LIST", instrument_list)

    # END INPUT DATA
    t1 = threading.Thread(target=start_server)
    t1.start()

    access_token_websocket = app_id + '-100' + ":" + access_token
    fs = ws.FyersSocket(access_token=access_token_websocket, run_background=False, log_path="./logs")
    fs.websocket_data = on_ticks

    fs.subscribe(symbol=instrument_list, data_type="symbolData")
    fs.keep_running()

    t1.join()
    print("websocket started !!")


if __name__ == "__main__":
    pass
