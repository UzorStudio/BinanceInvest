from binance.client import Client
from binance.exceptions import BinanceAPIException

import helpFunctions as hlp
import logging

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def Bye(symb,inv_sum,client,balance,price,total_balance):
    h = hlp.getminQty(symb)
    minInv =hlp.getMinInv(symb)
    sy = hlp.split_symbol(symb)
    s = hlp.split_symbol(symb)
    mx = hlp.market_lot_size(symb)

    if balance < minInv and inv_sum < minInv:
        return False

    cn = float(format(inv_sum / float(price), f".{h['lot_size'] + 1}f"))
    for tb in total_balance:
        if tb["asset"] == s['quoteAsset']:
            if float(tb['free']) < inv_sum and float(tb['free']) > minInv:
                cn= float(format(float(tb['free'])/ float(price), f".{h['lot_size'] + 1}f"))
                print(f"cn balance: {cn}")
            elif float(tb['free']) < inv_sum and float(tb['free']) < minInv:
                return False

    if balance < inv_sum:
        cn = float(format(float(balance)/ float(price), f".{h['lot_size'] + 1}f"))

    if cn > mx["maxQty"]:
        cn = float(mx["maxQty"])
    elif cn < minInv:
        cn = float(minInv)

    logging.info(f"Bye: Inv Sum:{inv_sum} Bye Sum:{cn} {s['baseAsset']}")
    if float(balance) < inv_sum:
        cn= float(format(float(balance), f".{h['lot_size'] + 1}f"))
        print(f"cn1 non balance: {cn}")

    if h['lot_size'] == 0:
        cn = int(cn)

    if float(balance) >= inv_sum:
        c = hlp.numFrontZero(cn)
        if c['count'] == 1 and c['count'] < 5:
            cn = float(cn)
            print(f"cn3:{cn}")
        logging.error(f"cn_final: {cn} symb:{symb} lot size: {h} ")
        try:
            order = client.order_limit_buy(
                symbol=symb,
                quantity=cn,
                price=toFixed(float(price),hlp.price_filter_zero_frotn_num(symb)+1)
            )
        except BinanceAPIException as e:
            logging.error(e.args)
            return False

        re = ({"bye": {"baseAsset": sy['baseAsset'], "count": order['origQty']},
                 "sell": {"quoteAsset":sy['quoteAsset'], "count":float(order['price'])*float(order['origQty'])},
                 "order":order})
        print(f"cn: {cn} bye:{re}")
        return re

def Sell(symb,inv_sum,client,total_balance,price):
    h = hlp.getminQty(symb)
    sy = hlp.split_symbol(symb)
    cn = float(format(inv_sum, f".{h['lot_size'] + 1}f"))
    mx = hlp.market_lot_size(symb)["maxQty"]
    if cn > mx:
        cn = int(mx)
    print(f"cn sell: {cn}")
    print(f"cn_final: {cn} symb:{symb} price: {price}")

    for tb in total_balance:
        if tb["asset"] == sy['baseAsset']:
            if float(tb['free']) < cn:
                cn = float(format(float(tb['free']), f".{h['lot_size'] + 1}f"))

    order = client.order_limit_sell(
        symbol=symb,
        quantity=cn,
        price=toFixed(float(price),hlp.price_filter_zero_frotn_num(symb)+1)
    )
    re = ({"sell":{"quoteAsset":sy['baseAsset'], "count":order['origQty']},
              "bye":{"baseAsset": sy['quoteAsset'], "count": float(order['price'])*float(order['origQty'])},
              "order":order})
    print(f"cn: {cn} sell:{re}")
    return re

def getOrder(type,symb,client):
    orders = []
    for ord in client.get_all_orders(symbol=symb, limit=10):
        if ord['type'] == type:
            orders.append(ord)
    return orders

def check_order(symb,ordId,client):
    result = client.get_order(
        symbol=symb,
        orderId=ordId)

    return result


def BuyOrder(symb,inv_sum,balance,price,client,total_balance):
    h = hlp.getminQty(symb)
    minInv = hlp.getMinInv(symb)
    sy = hlp.split_symbol(symb)
    mx = hlp.market_lot_size(symb)["maxQty"]

    if balance < minInv and inv_sum < minInv:
        return False

    cn = float(format(inv_sum / float(price), f".{h['lot_size'] + 1}f"))
    for tb in total_balance:
        if tb["asset"] == sy['quoteAsset']:
            if float(tb['free']) < inv_sum and float(tb['free']) > minInv:
                cn = float(format(float(tb['free']) / float(price), f".{h['lot_size'] + 1}f"))
                print(f"cn balance: {cn}")
            elif float(tb['free']) < inv_sum and float(tb['free']) < minInv:
                return False



    if cn > mx:
        cn = int(mx)

    s = hlp.split_symbol(symb)
    logging.info(f"Bye: Inv Sum:{inv_sum} Bye Sum:{cn} {s['baseAsset']}")
    if float(balance) < inv_sum:
        cn = float(format(float(balance), f".{h['lot_size'] + 1}f"))
        print(f"cn1 non balance: {cn}")

    if h['lot_size'] == 0:
        cn = int(cn)

    if float(balance) >= inv_sum:
        c = hlp.numFrontZero(cn)
        if c['count'] == 1 and c['count'] < 5:
            cn = int(cn)
            print(f"cn3:{cn}")
        try:
            order = client.order_limit_buy(
                symbol=symb,
                quantity=cn,
                price=toFixed(float(price),hlp.price_filter_zero_frotn_num(symb)+1)
            )
        except BinanceAPIException as e:
            logging.error(e.args)
            return False

        re = ({"bye": {"baseAsset": sy['baseAsset'], "count": order['origQty']},
               "sell": {"quoteAsset": sy['quoteAsset'], "count": float(order['price']) * float(order['origQty'])},
               "order": order})
        print(f"byeOrder: {re}")
        return re


#print(ByOrder(symb='XRPBTC',inv_sum=0.1,client=client,priceb=0.00002375))
#print(Bye("XRPBTC",0.1,client=client))
#for o in getOrder(type="LIMIT",symb="XRPBTC",client=client):
#    print(o)
#print(Sell("XRPBTC",10000,client=client))