from binance.client import Client
import helpFunctions as hlp
import logging

def Bye(symb,inv_sum,client):
    h = hlp.getminQty_test(symb)
    sy = hlp.split_symbol_test(symb)
    price = client.get_avg_price(symbol=symb)["price"]


    cn = float(format(inv_sum / float(price), f".{h['lot_size'] + 1}f"))
    print(f"cn1: {cn}")
    mx = hlp.market_lot_size_test(symb)["maxQty"]
    print(f"mx {mx}")
    if cn > mx:
        cn = int(mx)

    s = hlp.split_symbol_test(symb)
    logging.info(f"Bye: Inv Sum:{inv_sum} Bye Sum:{cn} {s['baseAsset']}")
    for b in client.get_account()['balances']:
        if b['asset'] == s["quoteAsset"] and float(b['free']) <= inv_sum:
            cn= float(format(float(b['free']-(b['free']*0.1)), f".{h['lot_size'] + 1}f"))
            print(f"cn1 non balance: {cn}")

    for b in client.get_account()['balances']:
        if b['asset'] == s['quoteAsset'] and float(b['free']) < inv_sum:
            return False
        elif b['asset'] == s['quoteAsset'] and float(b['free']) >= inv_sum:
            print(f"cn2: {cn} lot_size: {h}")
            c = hlp.numFrontZero(cn)
            print(f"c: {c}")
            if c['count'] == 1 and c['count'] < 5:
                cn = int(cn)
                print(f"cn3:{cn}")
            order = client.order_market_buy(
                symbol=symb,
                quantity=cn
            )
            return ({"bye": {"baseAsset": sy['baseAsset'], "count": order['executedQty']},
                     "sell": {"quoteAsset":sy['quoteAsset'], "count":order['cummulativeQuoteQty']},
                     "order":order})

def Sell(symb,inv_sum,client):
    h = hlp.getminQty_test(symb)
    sy = hlp.split_symbol_test(symb)
    cn = float(format(inv_sum, f".{h['lot_size'] + 1}f"))
    mx = hlp.market_lot_size_test(symb)["maxQty"]
    if cn > mx:
        cn = int(mx)
    print(f"cn sell: cn")

    order = client.order_market_sell(
        symbol=symb,
        quantity=cn
    )
    return  ({"sell":{"quoteAsset":sy['quoteAsset'], "count":order['cummulativeQuoteQty']},
              "bye":{"baseAsset": sy['baseAsset'], "count": order['executedQty']},
              "order":order})

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


def BuyOrder(symb,inv_sum,priceb,client):
    print(symb)
    h = hlp.getminQty_test(symb)
    sy = hlp.split_symbol_test(symb)
    price = client.get_avg_price(symbol=symb)["price"]
    cn = float(format(inv_sum / float(price), f".{h['lot_size'] + 1}f"))
    print(cn)
    logging.info(f"Order Bye: {priceb} {sy['baseAsset']}")
    for b in client.get_account()['balances']:
        if b['asset'] == sy["quoteAsset"] and float(b['free']) <= inv_sum:
            cn= float(format(float(b['free']), f".{h['lot_size'] + 1}f"))
            print(f"cn1 non balance: {cn}")

    for b in client.get_account()['balances']:
        if b['asset'] == sy['quoteAsset'] and float(b['free']) < inv_sum:
            return False
        elif b['asset'] == sy['quoteAsset'] and float(b['free']) >= inv_sum:
            order = client.order_limit_buy(
                symbol=symb,
                quantity=cn,
                price= '{:0.0{}f}'.format(priceb, 8)
            )
            return ({"bye": {"baseAsset": sy['baseAsset'], "count": order['origQty']},
                     "sell": {"quoteAsset": sy['quoteAsset'], "count": order['cummulativeQuoteQty']},
                     "order": order})


#print(ByOrder(symb='XRPBTC',inv_sum=0.1,client=client,priceb=0.00002375))
#print(Bye("XRPBTC",0.1,client=client))
#for o in getOrder(type="LIMIT",symb="XRPBTC",client=client):
#    print(o)
#print(Sell("XRPBTC",10000,client=client))