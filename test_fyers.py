import os

from fyers_api.Websocket import ws
from fyers_api import fyersModel

from pprint import pprint
from flask import Flask, request
import threading
from dotenv import load_dotenv


##############################################
#                   INPUT's                  #
##############################################
load_dotenv()

apiKey = os.environ.get('FYERS_CLIENT_ID')
accessToken = os.environ.get('ACCESS_TOKEN')

app_id = apiKey
access_token = accessToken
fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=app_id)

expiry = {
    "year": "23",
    "month": "8",
    "day": "17"
}

intExpiry = expiry["year"] + expiry["month"] + expiry["day"]
strikeList = []
instrumentList = []

# NIFTY
data = {
    "symbols": "NSE:NIFTY50-INDEX"
}
ltp = fyers.quotes(data=data)
a = ltp['d'][0]['v']['lp']

for i in range(-2, 2):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)
    strikeList.append(strike + 50)

print("STRIKE LIST: ", strikeList)

# Add Index
instrumentList.append('NSE:NIFTY50-INDEX')

# Add CE
for strike in strikeList:
    ltp_option = "NSE:NIFTY" + str(intExpiry) + str(strike) + "CE"
    instrumentList.append(ltp_option)

# Add PE
for strike in strikeList:
    ltp_option = "NSE:NIFTY" + str(intExpiry) + str(strike) + "PE"
    instrumentList.append(ltp_option)

strikeList = []
# BANKNIFTY
data = {
    "symbols": "NSE:NIFTYBANK-INDEX"
}
ltp = fyers.quotes(data=data)
a = ltp['d'][0]['v']['lp']

for i in range(-2, 2):
    strike = (int(a / 100) + i) * 100
    strikeList.append(strike)

# Add Index
instrumentList.append('NSE:NIFTYBANK-INDEX')

# Add CE
for strike in strikeList:
    ltp_option = "NSE:BANKNIFTY" + str(intExpiry) + str(strike) + "CE"
    instrumentList.append(ltp_option)

# Add PE
for strike in strikeList:
    ltp_option = "NSE:BANKNIFTY" + str(intExpiry) + str(strike) + "PE"
    instrumentList.append(ltp_option)

instrumentList1 = [
    "NSE:NIFTY50-INDEX",
    "NSE:NIFTYBANK-INDEX",
    "NSE:SBIN-EQ",
    "MCX:CRUDEOIL23AUGFUT"
]

instrumentList = instrumentList + instrumentList1
print("BELOW IS THE COMPLETE INSTRUMENT LIST")
print(instrumentList)
##############################################
print("!! Started getltpDict.py !!")

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


def main():
    t1 = threading.Thread(target=start_server)
    t1.start()

    access_token_websocket = app_id + ":" + access_token
    fs = ws.FyersSocket(access_token=access_token_websocket, run_background=False, log_path="./logs")
    fs.websocket_data = on_ticks
    fs.subscribe(symbol=instrumentList, data_type="symbolData")
    fs.keep_running()

    t1.join()
    print("websocket started !!")


if __name__ == "__main__":
    main()
