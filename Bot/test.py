import time
from datetime import datetime, timedelta
import helpFunctions as hlp
import base
from binance.client import Client
import bin_func
#{'_id': ObjectId('636631a0c254806799853cb9'), 'valute_par': 'TRXBTC', 'name': 'TRXBTC', 'sum_invest': 0.1, 'bye_lvl': 3e-06, 'sell_lvl': 3.05e-06, 'triger_lvl': 3.05e-06, 'valuecheck': 'min', 'check_time': 1, 'next_check': datetime.datetime(2022, 11, 7, 12, 43, 13, 531000), 'order': False, 'count_hev': 10000.0, 'last_bye': ObjectId('6368d2f995050ace7cce1208'), 'first_bye': ObjectId('6368d2f995050ace7cce1208'), 'spent': 0.03026493, 'order_id': 0, 'not_archive': True, 'triger': True, 'earned': 0}
#client = Client("b4V0IpllGxTYI0fUKVVRrALW8jV6hAqH0nkv37IHUyXjmu4sJbF6Mo7qHNkS3FnA","QNJEnRpzh8iuxwRQm8DLYHO7bB85TXGAut1xVBi95ynlHoVIGyKmzOotQLOwlCsM")
#db = base.Base("localhost")

#print(client.order_market_sell(symbol='TRXBTC',quantity=10000))

datecheck = datetime.now().time().second
print(datecheck)
time.sleep(5)
print(datetime.now().second)
print(datetime.now().second-datecheck)

#print(client.get_all_tickers())

#orders = client.get_open_orders(symbol='TRXUSDT')
#for o in orders:
#    client.cancel_order(symbol='TRXUSDT',orderId=o['orderId'])
#
##ord = bin_func.Sell(symb='TRXBTC',client=client,inv_sum=10000)
##
##

#


#while True:
#
#    for o in orders:
#        if o['type'] == 'LIMIT':
#            print(o)
#    print(client.get_avg_price(symbol='TRXBTC')['price'])
#    time.sleep(5)
#print(bin_func.BuyOrder(symb="TRXBTC",inv_sum=10000,client=client,))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#print(bin_func.Sell(symb="TRXBTC",inv_sum=10000,client=client))
#sy = hlp.split_symbol('JASMYBTC')
#h = hlp.getminQty('JASMYBTC')
#cn = 499
#free= 500
#for b in client.get_account()['balances']:
#    if b["asset"] == sy['baseAsset']:
#        print(f"{b['asset']} {sy['baseAsset']}")
#
#        if float(free) < cn:
#            cn = float(format(float(free), f".{h['lot_size'] + 1}f"))
#
#print(cn)

#db.postOperationSell(bot_id='63692d8e6bf67ef9ac674c0d',sell_lvl=3.05e-06,valute_par='TRXBTC',order="orderID",count=0.03)

#db = base.Base("localhost")
#
#print(db.getBot('636631a0c254806799853cb9'))
#
#db.postOperationSell(bot_id='636631a0c254806799853cb9',sell_lvl=3.05e-06,valute_par='TRXBTC',order="orderID",count=0.13)
#
#print(db.getBot('636631a0c254806799853cb9'))

#
#
#for b in client.get_account()['balances']:
#    if float(b['free']) > 0 :
#        print(b)



#from binance.client import Client
#import datetime
#import random
#from time import sleep
#import helpFunctions as hlp
#
#from binance.enums import SIDE_BUY, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
#
#import base
#

## order_bye = {'symbol': 'ETHBTC', 'orderId': 5911417, 'orderListId': -1, 'clientOrderId': 'aMFYXVYv9NrTfMNqyfpmmF', 'transactTime': 1667295841023, 'price': '0.00000000', 'origQty': '1.00000000', 'executedQty': '1.00000000', 'cummulativeQuoteQty': '0.07770588', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{'price': '0.07769100', 'qty': '0.03637000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349454}, {'price': '0.07769100', 'qty': '0.07504000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349455}, {'price': '0.07769300', 'qty': '0.06436000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349456}, {'price': '0.07770500', 'qty': '0.11325000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349457}, {'price': '0.07770600', 'qty': '0.10038000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349458}, {'price': '0.07770700', 'qty': '0.09781000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349459}, {'price': '0.07770800', 'qty': '0.09009000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349460}, {'price': '0.07770900', 'qty': '0.09008000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349461}, {'price': '0.07771000', 'qty': '0.07078000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349462}, {'price': '0.07771100', 'qty': '0.10681000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349463}, {'price': '0.07771300', 'qty': '0.06563000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349464}, {'price': '0.07771400', 'qty': '0.08940000', 'commission': '0.00000000', 'commissionAsset': 'ETH', 'tradeId': 349465}]}
#
#
#sum = 0
#
#for b in client.get_account()['balances']:
#    if float(b['free']) > 0:
#        print(b)
#
#
#order = client.create_test_order(
#    symbol="ETHUSDT",
#    side=SIDE_BUY,
#    type=ORDER_TYPE_LIMIT,
#    timeInForce=TIME_IN_FORCE_GTC,
#    quantity=1,
#    price=1538)
#
#print(order)
#
##for ord in client.get_all_orders(symbol="ETHUSDT", limit=10):
##    if ord['type'] == "LIMIT":
##        print(ord)
#
#
#
#
## В случае селл продает указанное количесвто первой валюты (тоесть покупает вторую )
## В случае бай покупает указанное количество первой валюты (тоесть продает вторую)
## Чтобы понять сколкьо продавать второй валюты нужно ВВ/ЦЕНА
#symb = 'XRPBTC'
#inv_sum = 0.1
#side="buy"
#
#
#
#
#if side == 'buy':
#    h = hlp.getminQty_test(symb)
#    sy = hlp.split_symbol_test(symb)
#    price = client.get_avg_price(symbol=symb)["price"]
#    print(f"price: {price}")
#    cn = float(format(inv_sum / float(price), f".{h['lot_size']+1}f"))
#    print(cn)
#    order = client.order_market_buy(
#       symbol=symb,
#       quantity=cn
#    )
#    print(order)
#    print(f"bye: {sy['baseAsset']} {order['executedQty']} sell: {sy['quoteAsset']} {inv_sum} {order['cummulativeQuoteQty']}")
#else:
#    h = hlp.getminQty_test(symb)
#    sy = hlp.split_symbol_test(symb)
#    cn = float(format(inv_sum, f".{h['lot_size'] + 1}f"))
#    print(cn)
#    order = client.order_market_sell(
#        symbol=symb,
#        quantity=cn
#    )
#    print(order)
#    print(f"sell: {sy['baseAsset']} {order['executedQty']} bye: {sy['quoteAsset']} {order['cummulativeQuoteQty']}")
## price =float(format(float(0.77457913/float(client.get_avg_price(symbol='ETHBTC')["price"])), ".8f"))
## print(price)
## order = client.order_market_sell(
##    symbol="USDTBTC",
##    quantity=price
## )
#
## 0.07636426
##print("-----------")
##print(order)
#  # количесвто купленной второй валюты
##for o in order['fills']:
##    sum += float(o['qty'])
#
## for o in order['fills']:
##    print(o)
#
#print("_____")
#
#for b in client.get_account()['balances']:
#    if float(b['free']) > 0:
#        print(b)

# print(client)
# db = base.Base("localhost")
# for h in db.getBotsBySymbol("WINBNB"):
#    print(len(str(h['sell_lvl']).split("e")) > 1)
#    if len(str(h['sell_lvl']).split("e")) > 1:
#        print(format(float(h['sell_lvl']), ".8f"))
#    else:
#        print(h['sell_lvl'])
# print(datetime.datetime.now().strftime('%Y-%m-%d'))

# orders = client.get_all_orders(symbol='BNBBTC', limit=10)
# print(orders)3.38e-06


# Количесвто нулей после запятой

# dollar = 10
# i = 0
# pr =[]
# while dollar <= 1000:
#    #profit = random.randint(5,21)/100
#    profit = 0.027
#    pr.append(profit)
#    #profit = 0.21
#    dollar = dollar+(dollar*profit)
#    i +=1
#    print(f"{dollar} {i} {profit}")
#
# print(sum(pr)/len(pr))
#
#
#
# info = client.get_account()['balances']
#
# for i in info:
#    if float(i['free']) > 0:
#        print(i)
