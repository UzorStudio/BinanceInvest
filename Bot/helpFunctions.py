import logging
from datetime import datetime, timedelta

from binance.client import Client
import json
import base
db = base.Base("mongodb://Roooasr:sedsaigUG12IHKJhihsifhaosf@mongodb:27017/")
#db = base.Base("localhost")

try:
    with open('exchange_info_test.json') as json_file:
        inf_test = json.load(json_file)
except Exception as e:
    print(f"exchange_info_test open err: {e.args}")




def cansle_order(order,client, trigger,price):
    try:
        if "updateTime" in order:
            time_order = datetime.fromtimestamp(int(order['updateTime']) / 1000)
        else:
            print(order)
            print("strenge error_______________")
            return 0
        print(f"cnsl_time:{time_order + timedelta(hours=1)} time_order:{time_order} time_now: {datetime.now()}")
        print(order)
    except:
        logging.error("str err____________________ cansle_order")
        return 0

    if trigger < price and 1-(trigger/price) > 0.02:
        if time_order + timedelta(hours=1) < datetime.now() and order['status'] == 'NEW':
            result = client.cancel_order(
                symbol=order['symbol'],
                orderId=str(order['orderId']))
            re = {"order":order,"res":result,"price":result['price'],"return":float(result['origQty'])*float(result['price']),"status": "NEW",'executedQty':result['executedQty']}
            print(f"cansle order:{re}")
            return re
        else:
            return 0
    else:
        return 0

def numFrontZero(num):
    num = list(str(float(num)).split(".")[1])
    count = len(num)
    return ({"count":count,"num":int("".join(num))})

def market_lot_size_test(symbol):
    for i in inf_test['symbols']:
        if i["symbol"] == symbol:
            for s in i["filters"]:
                #print(f"help: {s}")
                if s['filterType'] == 'MARKET_LOT_SIZE':
                    return {"minQty":float(s['minQty']),"maxQty":float(s['maxQty'])}


def market_lot_size(symbol):
    i = db.getSymbInfo(symbol)
    for s in i["filters"]:
        #print(f"help: {s}")
        if s['filterType'] == 'MARKET_LOT_SIZE':
            return {"minQty":float(s['minQty']),"maxQty":float(s['maxQty'])}


def split_symbol_test(symbol):
    for i in inf_test['symbols']:
        if i["symbol"] == symbol:
            return {'baseAsset':i['baseAsset'],'quoteAsset':i['quoteAsset']}


def split_symbol(symbol):
    i = db.getSymbInfo(symbol)
    return {'baseAsset':i['baseAsset'],'quoteAsset':i['quoteAsset']}

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def price_filter_zero_frotn_num_test(symbol):
    for i in inf_test['symbols']:
        if i["symbol"] == symbol:
            for s in i["filters"]:
                # print(f"help: {s}")
                if s['filterType'] == 'PRICE_FILTER':
                    return int(len(list(s['minPrice'].split("1")[0].replace("0.",""))))


def price_filter_zero_frotn_num(symbol):
    i = db.getSymbInfo(symbol)
    for s in i["filters"]:
        # print(f"help: {s}")
        if s['filterType'] == 'PRICE_FILTER':
            return int(len(list(s['minPrice'].split("1")[0].replace("0.",""))))

def getminQty_test(symbol):
    """Возвращает минимальную сумму покупки первой валюты"""

    for i in inf_test['symbols']:
        if i["symbol"] == symbol:
            for s in i["filters"]:
                #print(f"help: {s}")
                if s['filterType'] == 'LOT_SIZE':
                    return {"num":float(s['minQty']),"lot_size":len(s['minQty'].split("1")[0].replace('0.',""))}


def getminQty(symbol):
    """Возвращает минимальную сумму покупки первой валюты"""
    i = db.getSymbInfo(symbol)
    for s in i["filters"]:
        # print(f"help: {s}")
        if s['filterType'] == 'LOT_SIZE':
            return {"num": float(s['minQty']), "lot_size": len(s['minQty'].split("1")[0].replace('0.', ""))}

def getMinInv_test(symbol):
    for i in inf_test['symbols']:
        if i["symbol"] == symbol:
            for s in i["filters"]:

                if s['filterType'] == 'MIN_NOTIONAL':
                    return float(s['minNotional'])


def getMinInv(symbol):
    i = db.getSymbInfo(symbol)
    for s in i["filters"]:
        if s['filterType'] == 'MIN_NOTIONAL':
            return float(s['minNotional'])


def update(api_kay,api_secret,test_net_on):

    if test_net_on:
        client = Client(api_kay,
                        api_secret,
                        testnet=test_net_on)
        with open("exchange_info_test.json","w") as file:
           json.dump(client.get_exchange_info(),file)
    else:
        client = Client(api_kay,
                        api_secret,
                        testnet=test_net_on)
        with open("exchange_info.json", "w") as file:
            json.dump(client.get_exchange_info(), file)

#print(getminQty(client,'XRPBUSD'))
#print("____")
#print(getminQty(client,'BNBBTC'))