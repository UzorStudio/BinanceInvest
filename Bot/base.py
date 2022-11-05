import calendar

import pymongo
from bson import ObjectId

from datetime import datetime
from datetime import timedelta


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

    def regBot(self, valute_par, name, sum_invest, bye_lvl, sell_lvl, triger_lvl, valuecheck, check_time, triger):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        next_check = 0

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
            "valute_par": valute_par,
            "name": name,
            "sum_invest": float(sum_invest),
            "bye_lvl": float(bye_lvl),
            "sell_lvl": float(sell_lvl),
            "triger_lvl": float(triger_lvl),
            'valuecheck': valuecheck,
            'check_time': int(check_time),
            'next_check': datetime.now(),
            'order': False,
            "count_hev": 0,  # записывать количество
            'last_bye': "",  # Записывать id последней покупки
            'first_bye': "",  # Записывать id первой покупки
            'spent':0,
            "order_id":0,
            'not_archive': True,
            'triger': triger
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

    def reloadBot(self, id, sum_invest, bye_lvl, sell_lvl, triger_lvl, valuecheck, check_time, triger):
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
            'last_bye': Bots.find_one({"_id": ObjectId(id)})['last_bye'],  # Записывать id последней покупки
            'first_bye': Bots.find_one({"_id": ObjectId(id)})['first_bye'],  # Записывать id первой покупки
            'not_archive': Bots.find_one({"_id": ObjectId(id)})['not_archive'],
            'triger': triger
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

    def openSymbol(self):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        symbol = []
        symbol1= []
        for b in Bots.find({}):
            if b['valute_par'] not in symbol1:
                symbol.append({"symbol":b['valute_par'],"count_bot":len(list(Bots.find({"valute_par":b['valute_par']})))})
                symbol1.append(b['valute_par'])
            else:
                pass
        print(len(symbol))
        return symbol




    def postOperationBye(self, bot_id, bye_lvl, valute_par, count,order,spent):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        Bots = db["Bots"]

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

        Bots.update_one({"_id": bot_id}, {"$inc": {"count_hev": +count}})
        Bots.update_one({"_id": bot_id}, {"$inc": {"spent": +spent}})
        ids = Hist.insert_one(post).inserted_id
        if Bots.find_one({"_id": bot_id})['first_bye'] == "":
            Bots.update_one({"_id": bot_id}, {"$set": {"first_bye": ids}})
        Bots.update_one({"_id": bot_id}, {"$set": {"last_bye": ids}})

    def postOperationSell(self, bot_id, sell_lvl, valute_par, count,order):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        Bots = db["Bots"]
        bot = Bots.find_one({"_id": bot_id})


        spent = bot['spent']
        price_sell = count
        profit = 100 - ((spent / price_sell) * 100)

        post = {
            "lvl": sell_lvl,
            "valute_par": valute_par,
            "count": count,
            "type": "Продажа",
            "date": datetime.now(),
            "profit": profit,
            "bot_id": bot_id,
            "order":order
        }

        Bots.update_one({"_id": bot_id}, {"$inc": {"count_hev": -count}})
        Bots.update_one({"_id": bot_id}, {"$set": {"spent": 0}})
        Bots.update_one({"_id": bot_id}, {"$set": {"first_bye": ""}})
        Bots.update_one({"_id": bot_id}, {"$inc": {"sum_invest": (bot['sum_invest'] * (profit / 100))}})
        Hist.insert_one(post)

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


    def getOrderId(self,bot_id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]
        Hist = db["Hist"]

        try:
            return Hist.find_one({"order":{"orderId":Bots.find_one({"_id":ObjectId(bot_id)})['order_id']}})
        except:
            return 0

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