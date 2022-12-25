import calendar

import pymongo
from bson import ObjectId

from datetime import datetime
from datetime import timedelta


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

class Base:
    def __init__(self, classterMongo):
        self.classterMongo = classterMongo
        self.classter = pymongo.MongoClient(self.classterMongo)

    def botNextCheck(self, id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        bot = Bots.find_one({"_id": ObjectId(id)})

        if bot["valuecheck"] == 'min':
            next_check = datetime.now() + timedelta(minutes=int(bot["check_time"]))
        elif bot["valuecheck"] == 'hour':
            next_check = datetime.now() + timedelta(hours=int(bot["check_time"]))
        elif bot["valuecheck"] == 'dey':
            next_check = datetime.now() + timedelta(days=int(bot["check_time"]))
        elif bot["valuecheck"] == 'month':
            date = datetime.now()
            days_in_month = calendar.monthrange(date.year, date.month)[1]

            next_check = datetime.now() + timedelta(days=int(bot["check_time"]) * days_in_month)
        print(f"next check {next_check}")

        Bots.update_one({"_id": ObjectId(id)}, {"$set": {'next_check': next_check}})

    def regBot(self, valute_par, total_sum_invest,name, sum_invest, bye_lvl, sell_lvl, triger_lvl, valuecheck, check_time, triger):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        post = {
            "valute_par": valute_par,
            "name": name,
            "sum_invest": float(sum_invest),
            "total_sum_invest": float(total_sum_invest),
            "bye_lvl": float(bye_lvl),
            "sell_lvl": float(sell_lvl),
            "triger_lvl": float(triger_lvl),
            'valuecheck': valuecheck,
            'check_time': int(check_time),
            'next_check': datetime.now(),
            'order': False,
            'orders_bye': [],
            'orders_sell': [],
            "count_hev": 0,  # записывать количество
            'spent':0,
            'spent_true':0,
            "order_id":0,
            'not_archive': True,
            'triger': triger,
            "cikle_profit":0,
            "total_profit":0,
            "cikle_count":0,
            "base_sum_invest":float(sum_invest),
            "base_total_sum_invest":float(total_sum_invest),
            "earned": 0,
            "last_price":[]
        }

        return Bots.insert_one(post).inserted_id

    def delBot(self, id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.update_one({"_id": ObjectId(id)}, {"$set": {'not_archive': False}})

    def returnBot(self, id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.update_one({"_id": ObjectId(id)}, {"$set": {'not_archive': True}})

    def returnCountHev(self,bot_id,ret):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        print(f"bot:{bot_id} ret: {ret}")
        if ret['status'] == 'PARTIALLY_FILLED':
            Bots.update_one({"_id": ObjectId(bot_id)}, {"$inc": {'count_hev': +ret['executedQty'],'total_sum_invest': +ret['return']}})
        else:
            Bots.update_one({"_id":ObjectId(bot_id)},{"$inc":{'total_sum_invest':+ret['return']}})


    def ZeroBot(self):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        for bot in Bots.find({}):
            post = {
                "valute_par": bot["valute_par"],
                "name":  bot["valute_par"],
                "sum_invest":  bot["base_sum_invest"],
                "total_sum_invest":  bot["base_total_sum_invest"],
                "bye_lvl": bot["bye_lvl"],
                "sell_lvl": bot["sell_lvl"],
                "triger_lvl": bot["triger_lvl"],
                'valuecheck': bot["valuecheck"],
                'check_time': bot["check_time"],
                'next_check': datetime.now(),
                'order': False,
                'orders_bye': [],
                'orders_sell': [],
                "count_hev": 0,  # записывать количество
                'spent': 0,
                'spent_true': 0,
                "order_id": 0,
                'not_archive': True,
                'triger': bot["triger"],
                "cikle_profit": 0,
                "total_profit": 0,
                "cikle_count": bot["cikle_count"],
                "base_sum_invest": bot["base_sum_invest"],
                "base_total_sum_invest": bot["base_total_sum_invest"],
                "earned": bot["earned"],
                "last_price": []
            }

            Bots.update_one({"_id":ObjectId(bot["_id"])},{"$set":post})



    def reloadBot(self, id, sum_invest, bye_lvl,base_total_sum_invest, sell_lvl, triger_lvl, valuecheck, check_time, triger):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        if valuecheck == 'min':
            next_check = datetime.now() + timedelta(minutes=int(check_time))
        elif valuecheck == 'hour':
            next_check = datetime.now() + timedelta(hours=int(check_time))
        elif valuecheck == 'dey':
            next_check = datetime.now() + timedelta(days=int(check_time))
        elif valuecheck == 'month':
            date = datetime.now()
            days_in_month = calendar.monthrange(date.year, date.month)[1]

            next_check = datetime.now() + timedelta(days=int(check_time) * days_in_month)

        post = {
            "sum_invest": float(sum_invest),
            "bye_lvl": float(bye_lvl),
            "sell_lvl": float(sell_lvl),
            "triger_lvl": float(triger_lvl),
            'valuecheck': valuecheck,
            'check_time': int(check_time),
            'next_check': next_check,
            'order': Bots.find_one({"_id": ObjectId(id)})['order'],
            "count_hev": Bots.find_one({"_id": ObjectId(id)})['count_hev'],  # записывать количество
            'not_archive': Bots.find_one({"_id": ObjectId(id)})['not_archive'],
            'base_total_sum_invest': float(base_total_sum_invest),
            'triger': triger,
        }

        Bots.update_one({"_id": ObjectId(id)}, {"$set": post})

    def getBot(self, id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        return Bots.find_one({"_id": ObjectId(id)})

    def getAllBots(self):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        return Bots.find({})

    def getBotsBySymbol(self,symbol):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        return Bots.find({"valute_par":symbol})

    def setLastPrice(self,bot_id,price):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        print(f"last_price: {price} bot: {bot_id}")

        Bots.update_one({"_id": ObjectId(bot_id)},{"$push":{"last_price":price}})

    def dropLastPrice(self,bot_id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.update_one({"_id": ObjectId(bot_id)},{"$set":{"last_price":[]}})

    def dropLastPriceForPrice(self,bot_id,price):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        prices = Bots.find_one({"_id": ObjectId(bot_id)})['last_price']
        for pr in prices:
            if price == pr:
                prices.remove(pr)
                Bots.find_one({"_id": ObjectId(bot_id)},{"$set":{"last_price":prices}})

    def setTriger(self,bot_id,triger):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        Bots.update_one({"_id": ObjectId(bot_id)},{"$set":{"order":triger}})
    def openSymbol(self):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        symbol = []
        symbol1= []
        for b in Bots.find({}):
            if b['valute_par'] not in symbol1:
                price_massive_bye = []
                price_massive_sell = []
                for prices in Bots.find({"valute_par":b['valute_par']}):
                    price_massive_bye.append(prices['bye_lvl'])
                    price_massive_sell.append(prices['sell_lvl'])

                symbol.append({"symbol":b['valute_par'],"max_bye":max(price_massive_bye),"max_sell":max(price_massive_sell),"min_bye":min(price_massive_bye),"min_sell":min(price_massive_sell),"count_bot":len(list(Bots.find({"valute_par":b['valute_par']})))})
                symbol1.append(b['valute_par'])
            else:
                pass
        print(len(symbol))
        return symbol


    def ByeForBot(self, bot_id,order,spent):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.update_one({"_id": bot_id}, {"$inc": {"spent": +spent,
                                                   'total_sum_invest': -spent
                                                   }})
        Bots.update_one({"_id": bot_id}, {"$push":{"orders_bye":order['order']['orderId']}})


    def SellForBot(self, bot_id, order,spent):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        bot = Bots.find_one({"_id": ObjectId(bot_id)})

        Bots.update_one({"_id": ObjectId(bot_id)}, {"$inc": {"count_hev": -float(order['sell']['count']),"spent_true": -spent}})
        Bots.update_one({"_id": ObjectId(bot_id)},
                        {"$push": {"orders_sell": {"id": order['order']['orderId'], "spents": float(spent),"be_bye":bot["last_price"]}}})


    def UpdateSymbolInfo(self,client):
        inf = client.get_exchange_info()
        db = self.classter["BinanceInvest"]
        Symbols = db["Symbols"]
        Symbols.delete_many({})

        for i in inf['symbols']:
            Symbols.insert_one(i)

    def UpdateTikers(self,client):
        tick = client.get_all_tickers()
        db = self.classter["BinanceInvest"]
        Tickers = db["Tickers"]

        for i in tick:
            Tickers.insert_one(i)

    def getAllTickers(self):
        db = self.classter["BinanceInvest"]
        Tickers = db["Tickers"]

        return Tickers.find({})

    def getSymbInfo(self,symb):
        db = self.classter["BinanceInvest"]
        Symbols = db["Symbols"]

        return Symbols.find_one({"symbol":symb})

    def dropOrderId(self,bot_id,res):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        bot = Bots.find_one({"_id": ObjectId(bot_id)})
        orders_sell = bot['orders_sell']
        orders_bye = bot['orders_bye']
        if res['order']['side'] == 'BUY':
            for o in orders_bye:
                if o == res['order']['orderId']:
                    orders_bye.remove(o)
                    Bots.update_one({"_id": ObjectId(bot_id)}, {"$set":{'orders_bye':orders_bye}})

        if res['order']['side'] == 'SELL':
            for o in orders_sell:
                if o['id'] == res['order']['orderId']:
                    orders_sell.remove(o)
                    Bots.update_one({"_id": ObjectId(bot_id)}, {"$set":{'orders_sell':orders_sell}})


    def postOperationBye(self, bot_id, bye_lvl, valute_par, count,order,spent):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        Bots = db["Bots"]
        bot = Bots.find_one({"_id": ObjectId(bot_id)})
        post = {
            "lvl": bye_lvl,
            "valute_par": valute_par,
            "count": count,
            "type": "Покупка",
            "date": datetime.now(),
            "profit": 0,
            "bot_id": bot_id,
            "order":order,
            "spent":spent
        }
        for o in bot['orders_bye']:
            if o == order['orderId']:
                ord = bot['orders_bye']
                ord.remove(o)
                Bots.update_one({"_id": ObjectId(bot_id)}, {"$set":{'orders_bye':ord}})
        Bots.update_one({"_id": ObjectId(bot_id)}, {"$inc":{"count_hev": +count,"spent_true": +spent}})
        Bots.update_one({"_id": ObjectId(bot_id)}, {"$inc":{}})
        Hist.insert_one(post)




    def postOperationSell(self, bot_id, sell_lvl, valute_par, count, order,spent):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        Bots = db["Bots"]
        bot = Bots.find_one({"_id": ObjectId(bot_id)})
        ern = (float(count) - float(spent))/2
        print(f"ern: {ern}")
        count = float(count) - ern

        profit = (1-(spent/float(count)))*100

        total_percent = (1-(bot['base_sum_invest']/(bot['sum_invest']+(bot['sum_invest'] * (profit / 100)))))*100
        print("sell: _____________start")
        print(bot)
        print(order)
        print(f"profit {profit} total_profit {total_percent}")
        print(f"spent {spent} count {count}")
        print(f"erned: {(float(count) - float(spent))}")
        print(f"New sum_invest: {bot['sum_invest']+(bot['sum_invest'] * (profit / 100))}")
        print(f"New Total_sum_invest: {bot['base_total_sum_invest']+bot['base_total_sum_invest']* (profit / 100)}")
        print("sell: _____________end")

        post = {
            "lvl": sell_lvl,
            "valute_par": valute_par,
            "count": count,
            "type": "Продажа",
            "date": datetime.now(),
            "profit": profit,
            "bot_id": bot_id,
            "order":order,
            "spent":order['executedQty']
        }
        ord = bot['orders_sell']
        for o in bot['orders_sell']:
            if o['id'] == order['orderId']:
                print(f"1o: {o}, ord: {ord}")
                ord.remove(o) # работает
                print(f"1o: {o}, ord: {ord}")
                Bots.update_one({"_id": ObjectId(bot_id)}, {"$set":{'orders_sell':ord}})
        if ern > 0:
            Bots.update_one({"_id": ObjectId(bot_id)}, {"$inc": {"sum_invest": +(bot['sum_invest'] * (profit / 100)),
                                                             "earned": +float(toFixed((float(count) - float(spent)),8)),
                                                             "cikle_count": +1
                                                             }})
            Bots.update_one({"_id": ObjectId(bot_id)}, {"$set": {"cikle_profit": profit,
                                                             "spent": bot['spent']-float(spent),
                                                             "total_profit": total_percent,
                                                             'total_sum_invest':bot['base_total_sum_invest']+(bot['base_total_sum_invest']* (profit / 100))
                                                             }})
        else:
            Bots.update_one({"_id": ObjectId(bot_id)}, {"$set": {"spent": bot['spent'] - float(spent)}})
        Hist.insert_one(post)
        return ern

    def postOperationOrgerBy(self, bye_lvl, valute_par, count, bot_id, orger_id,orger):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        Bots = db["Bots"]

        post = {
            "lvl": bye_lvl,
            "valute_par": valute_par,
            "count": count,
            "type": "Ордер на закупку",
            "date": datetime.now(),
            "profit": 0,
            "bot_id": bot_id,
            "order":orger

        }

        Hist.insert_one(post)
        Bots.update_one({"_id": bot_id}, {"$set": {"order": orger_id}})

    def setOrder(self, bot_id, status,order_id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.update_one({"_id": bot_id}, {"$set": {"order_id": order_id}})
        Bots.update_one({"_id": bot_id}, {"$set": {"order": status}})


    def getOrdersSellBot(self,bot_id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]


        return Bots.find_one({"_id":ObjectId(bot_id)})['orders_sell']


    def getOrdersByeBot(self,bot_id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]


        return Bots.find_one({"_id":ObjectId(bot_id)})['orders_bye']


    def cancelOrderSell(self,origQty,bot_id,orderId):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        ord = Bots.find_one({"_id":ObjectId(bot_id)})['orders_sell']
        spent = 0
        for o in ord:
            if o['id'] == orderId:
                ord.remove(o)  # работает
                spent = o['spents']
                Bots.update_one({"_id": ObjectId(bot_id)}, {"$set": {'orders_sell': ord}})


        Bots.update_one({"_id": ObjectId(bot_id)}, {"$inc":{"count_hev": +float(origQty),"spent_true": +spent}})


    def MustBeSend(self,summ,quoteAsset):
        db = self.classter["BinanceInvest"]
        MustBeDo = db["MustBeDo"]

        MustBeDo.insert_one({"type":"send","sum":summ,"quoteAsset":quoteAsset})

    def getMustBeSend(self,quoteAsset):
        db = self.classter["BinanceInvest"]
        MustBeDo = db["MustBeDo"]
        all = MustBeDo.find({"type":'send',"quoteAsset":quoteAsset})
        erns = 0
        for a in all:
            erns+=float(a['sum'])

        return erns

    def dellMustBseSend(self):
        db = self.classter["BinanceInvest"]
        MustBeDo = db["MustBeDo"]
        MustBeDo.delete_many({})
    def cancelOrderBye(self, order, bot_id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        ord = Bots.find_one({"_id": ObjectId(bot_id)})['orders_bye']
        for o in ord:
            if o == order['orderId']:
                ord.remove(o)  # работает
                Bots.update_one({"_id": ObjectId(bot_id)}, {"$set": {'orders_bye': ord}})

        Bots.update_one({"_id":ObjectId(bot_id)},{"$inc":{'total_sum_invest':+(order['origQty']*order['price'])}})

    def addCountHevOnOrder(self,bot_id,count):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.update_one({"_id": bot_id}, {"$inc": {"count_hev": +count}})

    def getAllHist(self):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        return reversed(list(Hist.find({})))

    def getHistToDey(self):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        return reversed(list(Hist.find({"date": {"$lte": datetime.now(),
                                                 "$gte": (datetime.now() - timedelta(days=1)).replace(microsecond=0,
                                                                                                      hour=0, minute=0,
                                                                                                      second=0)}})))

    def getHistByDay(self, date):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        trday = (datetime.now() - timedelta(days=(datetime.now() - datetime.strptime(date, '%Y-%m-%d')).days)).replace(
            microsecond=0, hour=0, minute=0, second=0)
        print(trday - timedelta(days=1))
        print(trday)
        return reversed(list(Hist.find({"date": {"$lte": trday + timedelta(days=1),
                                                 "$gte": trday}})))

    def getHistByBotId(self, id):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        return reversed(list(Hist.find({"bot_id": ObjectId(id), "date":
            {"$lte": datetime.now(),
             "$gte": (datetime.now() - timedelta(days=1)).replace(
                 microsecond=0, hour=0, minute=0, second=0)}})))

    def getHistByBotIdDate(self, id, date):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        trday = (datetime.now() - timedelta(days=(datetime.now() - datetime.strptime(date, '%Y-%m-%d')).days)).replace(
            microsecond=0, hour=0, minute=0, second=0)

        return reversed(list(Hist.find({"bot_id": ObjectId(id), "date": {"$lte": trday + timedelta(days=1),
                                                                         "$gte": trday}})))

    def openHistBotDate(self,id):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        date = []
        for d in Hist.find({"bot_id": ObjectId(id)}):
            if d['date'].strftime('%Y-%m-%d') not in date:
                date.append(d['date'].strftime('%Y-%m-%d'))
            else:
                pass
        return date


    def getHistByProcDayBot(self, prof, date,id):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        trday = (datetime.now() - timedelta(days=(datetime.now() - datetime.strptime(date, '%Y-%m-%d')).days)).replace(
            microsecond=0, hour=0, minute=0, second=0)

        return reversed(list(Hist.find({"profit": {"$lte": prof, "$gt": 0},
                                        "date": {"$lte": trday + timedelta(days=1),
                                                 "$gte": trday},
                                        "bot_id":ObjectId(id)})))


    def getHistByProcBot(self, prof,id):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        return reversed(list(Hist.find({"profit": {"$lte": prof, "$gt": 0},
                                        "date":
                                            {"$lte": datetime.now(),
                                             "$gte": (datetime.now() - timedelta(days=1)).replace(
                                                 microsecond=0, hour=0, minute=0, second=0)},
                                        "bot_id":ObjectId(id)})))





    def getHistByProc(self, prof):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        return reversed(list(Hist.find({"profit": {"$lte": prof, "$gt": 0},
                                        "date":
                                            {"$lte": datetime.now(),
                                             "$gte": (datetime.now() - timedelta(days=1)).replace(
                                                 microsecond=0, hour=0, minute=0, second=0)}})))

    def getHistByProcDay(self, prof, date):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        trday = (datetime.now() - timedelta(days=(datetime.now() - datetime.strptime(date, '%Y-%m-%d')).days)).replace(
            microsecond=0, hour=0, minute=0, second=0)

        return reversed(list(Hist.find({"profit": {"$lte": prof, "$gt": 0},
                                        "date": {"$lte": trday + timedelta(days=1),
                                                 "$gte": trday}})))


    def openHistByProc(self,prof):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        date = []

        for d in Hist.find({}):
            if d['date'].strftime('%Y-%m-%d') not in date and d['profit'] <= float(prof) and d['profit'] > 0:
                date.append(d['date'].strftime('%Y-%m-%d'))
            else:
                pass
        return date

    def openHistDate(self):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        date = []
        for d in Hist.find({}):
            if d['date'].strftime('%Y-%m-%d') not in date:
                date.append(d['date'].strftime('%Y-%m-%d'))
            else:
                pass
        return date