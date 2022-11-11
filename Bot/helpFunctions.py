from binance.client import Client
import json

try:
    with open('exchange_info_test.json') as json_file:
        inf_test = json.load(json_file)
except Exception as e:
    print(f"exchange_info_test open err: {e.args}")

try:
    with open('exchange_info.json') as json_file:
        inf = json.load(json_file)
except:
    print("exchange_info open err")


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

def split_symbol_test(symbol):
    for i in inf_test['symbols']:
        if i["symbol"] == symbol:
            return {'baseAsset':i['baseAsset'],'quoteAsset':i['quoteAsset']}

def split_symbol(symbol):
    for i in inf['symbols']:
        if i["symbol"] == symbol:
            return {'baseAsset':i['baseAsset'],'quoteAsset':i['quoteAsset']}

def getminQty_test(symbol):
    """Возвращает минимальную сумму покупки первой валюты"""

    for i in inf_test['symbols']:
        if i["symbol"] == symbol:
            print(f"help: {i}")
            for s in i["filters"]:
                #print(f"help: {s}")
                if s['filterType'] == 'LOT_SIZE':
                    return {"num":float(s['minQty']),"lot_size":len(s['minQty'].split("1")[0].replace('0.',""))}


def getminQty(symbol):
    """Возвращает минимальную сумму покупки первой валюты"""
    for i in inf['symbols']:
        if i["symbol"] == symbol:
            #print(f"help: {i}")
            for s in i["filters"]:
                #print(f"help: {s}")
                if s['filterType'] == 'LOT_SIZE':
                    return {"num":float(s['minQty']),"lot_size":len(s['minQty'].split("1")[0].replace('0.',""))}

def getMinInv_test(symbol):
    for i in inf_test['symbols']:
        if i["symbol"] == symbol:
            for s in i["filters"]:

                if s['filterType'] == 'MIN_NOTIONAL':
                    return float(s['minNotional'])


def getMinInv(symbol):
    for i in inf['symbols']:
        if i["symbol"] == symbol:
            for s in i["filters"]:

                if s['filterType'] == 'LOT_SIZE':
                    return float(s['minQty'])


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