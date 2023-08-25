# DISCLAIMER:
# 1) This sample code is for learning purposes only.
# 2) Always be very careful when dealing with codes in which you can place orders in your account.
# 3) The actual results may or may not be similar to backtested results. The historical results do not guarantee any profits or losses in the future.
# 4) You are responsible for any losses/profits that occur in your account in case you plan to take trades in your account.
# 5) TFU and Aseem Singhal do not take any responsibility of you running these codes on your account and the corresponding profits and losses that might occur.
# 6) The running of the code properly is dependent on a lot of factors such as internet, broker, what changes you have made, etc. So it is always better to keep checking the trades as technology error can come anytime.
# 7) This is NOT a tip providing service/code.
# 8) This is NOT a software. Its a tool that works as per the inputs given by you.
# 9) Slippage is dependent on market conditions.
# 10) Option trading and automatic API trading are subject to market risks

import datetime
import time
import pandas as pd
from fyers_api import accessToken
from fyers_api import fyersModel
import requests
from settings import Settings

####################__INPUT__#####################
st = Settings()

client_id = st.app_id
access_token = st.access_token
fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=client_id, log_path="./logs")

# TIME TO FIND THE STRIKE
entryHour = 9
entryMinute = 30
entrySecond = 0
startTime = datetime.time(entryHour, entryMinute, entrySecond)

stock = "NIFTY"  # BANKNIFTY OR NIFTY
otm = 100  # If you put -100, that means its 100 points ITM.
SL_point = 20
PnL = 0
df = pd.DataFrame(columns=['Date', 'CE_Entry_Price', 'CE_Exit_Price', 'PE_Entry_Price', 'PE_Exit_Price', 'PnL'])
df["Date"] = [datetime.date.today()]
premium = 0

# Time
# Find NSE price . If nse price < yesterday closing (ATM)
# Entry Price BUY
# Exit SL == target


expiry = {
    "year": "23",
    "month": "8",
    "day": "24",

    # YYMDD  22O06  22OCT  22OCT YYMMM
    # YYMMM  22, N, OV
    # YYMDD   22 o/n/d   03
    # YYMDD  22  6  10   22JUN
}

clients = [
    {
        "broker": "Fyers",
        "userID": "",
        "apiKey": "",
        "accessToken": "",
        "qty": 50  # this is not lot, 50 qty is 1 lot
    }
]


##################################################


def findStrikePriceATM():
    print(" Placing Orders ")
    global clients
    global SL_percentage

    if stock == "BANKNIFTY":
        name = "NSE:" + "NIFTYBANK-INDEX"  # "NSE:NIFTY BANK"
    elif stock == "NIFTY":
        name = "NSE:" + "NIFTY50-INDEX"  # "NSE:NIFTY 50"
    # TO get feed to Nifty: "NSE:NIFTY 50" and banknifty: "NSE: NIFTY BANK"

    strikeList = []

    prev_diff = 10000
    closest_Strike = 10000

    intExpiry = expiry["year"] + expiry["month"] + expiry["day"]  # 22OCT

    ######################################################
    # FINDING ATM
    ltp = getLTP(name)


    if stock == "BANKNIFTY":
        closest_Strike = int(round((ltp / 100), 0) * 100)
        print(closest_Strike)

    elif stock == "NIFTY":
        closest_Strike = int(round((ltp / 50), 0) * 50)
        print(closest_Strike)

    print("closest", closest_Strike)
    closest_Strike_CE = closest_Strike + otm
    closest_Strike_PE = closest_Strike - otm

    if stock == "BANKNIFTY":
        atmCE = "NSE:BANKNIFTY" + str(intExpiry) + str(closest_Strike_CE) + "CE"
        atmPE = "NSE:BANKNIFTY" + str(intExpiry) + str(closest_Strike_PE) + "PE"
    elif stock == "NIFTY":
        atmCE = "NSE:NIFTY" + str(intExpiry) + str(closest_Strike_CE) + "CE"
        atmPE = "NSE:NIFTY" + str(intExpiry) + str(closest_Strike_PE) + "PE"

    print(atmCE)
    print(atmPE)

    takeEntry(closest_Strike_CE, closest_Strike_PE, atmCE, atmPE)


def findStrikePricePremium():
    print(" Placing Orders ")
    global clients
    global SL_percentage
    global premium

    if stock == "BANKNIFTY":
        name = "NSE:" + "NIFTYBANK-INDEX"  # "NSE:NIFTY BANK"
    elif stock == "NIFTY":
        name = "NSE:" + "NIFTY50-INDEX"  # "NSE:NIFTY 50"

    strikeList = []

    prev_diff = 10000
    closest_Strike = 10000

    intExpiry = expiry["year"] + expiry["month"] + expiry["day"]

    ######################################################
    # FINDING ATM
    ltp = getLTP(name)
    if stock == "BANKNIFTY":
        for i in range(-8, 8):
            strike = (int(ltp / 100) + i) * 100
            strikeList.append(strike)
        print(strikeList)

        # FOR CE
        prev_diff = 10000
        for strike in strikeList:
            ltp_option = getLTP("NSE:BANKNIFTY" + str(intExpiry) + str(strike) + "CE")
            diff = abs(ltp_option - premium)
            print("diff==>", diff)
            if (diff < prev_diff):
                closest_Strike_CE = strike
                prev_diff = diff
        #  time.sleep(.5)

        # FOR PE
        prev_diff = 10000
        for strike in strikeList:
            ltp_option = getLTP("NSE:BANKNIFTY" + str(intExpiry) + str(strike) + "PE")
            diff = abs(ltp_option - premium)
            print("diff==>", diff)
            if (diff < prev_diff):
                closest_Strike_PE = strike
                prev_diff = diff
        #  time.sleep(.5)


    elif stock == "NIFTY":
        for i in range(-5, 5):
            strike = (int(ltp / 100) + i) * 100
            strikeList.append(strike)
            strikeList.append(strike + 50)
        print(strikeList)

        # For CE
        prev_diff = 10000
        for strike in strikeList:
            ltp_option = getLTP("NSE:NIFTY" + str(intExpiry) + str(strike) + "CE")
            diff = abs(ltp_option - premium)
            print("diff==>", diff)
            if (diff < prev_diff):
                closest_Strike_CE = strike
                prev_diff = diff
        #  time.sleep(.5)

        # For PE
        prev_diff = 10000
        for strike in strikeList:
            ltp_option = getLTP("NSE:NIFTY" + str(intExpiry) + str(strike) + "PE")
            diff = abs(ltp_option - premium)
            print("diff==>", diff)
            if (diff < prev_diff):
                closest_Strike_PE = strike
                prev_diff = diff
        #   time.sleep(.5)

    print("closest CE", closest_Strike_CE)
    print("closest PE", closest_Strike_PE)

    if stock == "BANKNIFTY":
        atmCE = "NSE:BANKNIFTY" + str(intExpiry) + str(closest_Strike_CE) + "CE"
        atmPE = "NSE:BANKNIFTY" + str(intExpiry) + str(closest_Strike_PE) + "PE"
    elif stock == "NIFTY":
        atmCE = "NSE:NIFTY" + str(intExpiry) + str(closest_Strike_CE) + "CE"
        atmPE = "NSE:NIFTY" + str(intExpiry) + str(closest_Strike_PE) + "PE"

    print(atmCE)
    print(atmPE)

    takeEntry(closest_Strike_CE, closest_Strike_PE, atmCE, atmPE)


def takeEntry(closest_Strike_CE, closest_Strike_PE, atmCE, atmPE):
    global SL_point
    global PnL
    ce_entry_price = getLTP(atmCE)
    pe_entry_price = getLTP(atmPE)
    PnL = ce_entry_price + pe_entry_price
    print("Current PnL is: ", PnL)
    df['CE_Entry_Price'] = [ce_entry_price]
    df['PE_Entry_Price'] = [pe_entry_price]

    print(" closest_CE ATM ", closest_Strike_CE, " CE Entry Price = ", ce_entry_price)
    print(" closest_PE ATM", closest_Strike_PE, " PE Entry Price = ", pe_entry_price)

    ceSL = round(ce_entry_price + SL_point, 1)
    peSL = round(pe_entry_price + SL_point, 1)
    print("Placing Order CE Entry Price = ", ce_entry_price, "|  CE SL => ", ceSL)
    print("Placing Order PE Entry Price = ", pe_entry_price, "|  PE SL => ", peSL)

    # SELL AT MARKET PRICE
    for client in clients:
        print("\n============_Placing_Trades_=====================")
        print("userID = ", client['userID'])
        broker = client['broker']
        uid = client['userID']
        key = client['apiKey']
        token = client['accessToken']
        qty = client['qty']

        oidentryCE = 0
        oidentryPE = 0

        oidentryCE = placeOrderFyers(atmCE, "SELL", qty, "MARKET", ce_entry_price, "regular")
        oidentryPE = placeOrderFyers(atmPE, "SELL", qty, "MARKET", pe_entry_price, "regular")

        print("The OID of Entry CE is: ", oidentryCE)
        print("The OID of Entry PE is: ", oidentryPE)

        exitPosition(atmCE, ceSL, ce_entry_price, atmPE, peSL, pe_entry_price, qty)


def exitPosition(atmCE, ceSL, ce_entry_price, atmPE, peSL, pe_entry_price, qty):
    global PnL
    traded = "No"

    while traded == "No":
        dt = datetime.datetime.now()
        try:
            ltp = getLTP(atmCE)
            ltp1 = getLTP(atmPE)
            if ((ltp > ceSL) or (dt.hour >= 15 and dt.minute >= 15)) and ltp != -1:
                oidexitCE = placeOrderFyers(atmCE, "BUY", qty, "MARKET", ceSL, "regular")
                PnL = PnL - ltp
                print("Current PnL is: ", PnL)
                df["CE_Exit_Price"] = [ltp]
                print("The OID of Exit CE is: ", oidexitCE)
                traded = "CE"
            elif ((ltp1 > peSL) or (dt.hour >= 15 and dt.minute >= 15)) and ltp1 != -1:
                oidexitPE = placeOrderFyers(atmPE, "BUY", qty, "MARKET", peSL, "regular")
                PnL = PnL - ltp1
                print("Current PnL is: ", PnL)
                df["PE_Exit_Price"] = [ltp1]
                print("The OID of Exit PE is: ", oidexitPE)
                traded = "PE"
            else:
                print("NO SL is hit")
                time.sleep(1)

        except:
            print("Couldn't find LTP , RETRYING !!")
            time.sleep(1)

    if (traded == "CE"):
        peSL = pe_entry_price
        while traded == "CE":
            dt = datetime.datetime.now()
            try:
                ltp = getLTP(atmPE)
                if ((ltp > peSL) or (dt.hour >= 15 and dt.minute >= 15)) and ltp != -1:
                    oidexitPE = placeOrderFyers(atmPE, "BUY", qty, "MARKET", peSL, "regular")
                    PnL = PnL - ltp
                    print("Current PnL is: ", PnL)
                    df["PE_Exit_Price"] = [ltp]
                    print("The OID of Exit PE is: ", oidexitPE)
                    traded = "Close"
                else:
                    print("PE SL not hit")
                    time.sleep(1)

            except:
                print("Couldn't find LTP , RETRYING !!")
                time.sleep(1)

    elif (traded == "PE"):
        ceSL = ce_entry_price
        while traded == "PE":
            dt = datetime.datetime.now()
            try:
                ltp = getLTP(atmCE)
                if ((ltp > ceSL) or (dt.hour >= 15 and dt.minute >= 15)) and ltp != -1:
                    oidexitCE = placeOrderFyers(atmCE, "BUY", qty, "MARKET", ceSL, "regular")
                    PnL = PnL - ltp
                    df["CE_Exit_Price"] = [ltp]
                    print("Current PnL is: ", PnL)
                    print("The OID of Exit CE is: ", oidexitCE)
                    traded = "Close"
                else:
                    print("CE SL not hit")
                    time.sleep(1)
            except:
                print("Couldn't find LTP , RETRYING !!")
                time.sleep(1)

    elif (traded == "Close"):
        print("All trades done. Exiting Code")


def getLTP(instrument):
    url = "http://localhost:4001/ltp?instrument=" + instrument
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    data = resp.json()
    return data


def checkTime_tofindStrike():
    x = 1
    while x == 1:
        dt = datetime.datetime.now()
        # if( dt.hour >= entryHour and dt.minute >= entryMinute and dt.second >= entrySecond ):
        if (dt.time() >= startTime):
            print("time reached")
            x = 2
            findStrikePriceATM()
        else:
            time.sleep(.1)
            print(dt, " Waiting for Time to check new ATM ")


def placeOrderFyers(inst, t_type, qty, order_type, price, variety):
    exch = inst[:3]
    symb = inst[4:]
    dt = datetime.datetime.now()
    papertrading = 0  # if this is 1, then actual trades will get placed
    print(dt.hour, ":", dt.minute, ":", dt.second, " => ", t_type, " ", symb, " ", qty, " ", order_type, " @ price =  ",
          price)
    if (order_type == "MARKET"):
        type1 = 2
        price = 0
    elif (order_type == "LIMIT"):
        type1 = 1

    if (t_type == "BUY"):
        side1 = 1
    elif (t_type == "SELL"):
        side1 = -1

    data = {
        "symbol": inst,
        "qty": qty,
        "type": type1,
        "side": side1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
        "stopLoss": 0,
        "takeProfit": 0
    }
    try:
        if (papertrading == 1):
            orderid = fyers.place_order(data)
            print(dt.hour, ":", dt.minute, ":", dt.second, " => ", symb, orderid)
            return orderid
        else:
            return 0


    except Exception as e:
        print(dt.hour, ":", dt.minute, ":", dt.second, " => ", symb, "Failed : {} ".format(e))


checkTime_tofindStrike()
df["PnL"] = [PnL]
df.to_csv('Str1_Fyers_websocket.csv', mode='a', index=True, header=True)
