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
            'not_archive':True,
            'triger': triger
        }

        return Bots.insert_one(post).inserted_id

    def delBot(self, id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.update_one({"_id": ObjectId(id)},{"$set":{'not_archive':False}})

    def returnBot(self, id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.update_one({"_id": ObjectId(id)},{"$set":{'not_archive':True}})

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
            "count_hev": Bots.find_one({"_id": ObjectId(id)})['count_hev'], # записывать количество
            'last_bye':Bots.find_one({"_id": ObjectId(id)})['last_bye'], # Записывать id последней покупки
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

    def postOperationBye(self, bot_id, bye_lvl, valute_par, count):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        Bots = db["Bots"]

        post = {
            "lvl": bye_lvl,
            "valute_par": valute_par,
            "count": count,
            "type":"Покупка",
            "date":datetime.now(),
            "profit":0,
            "bot_id":bot_id

        }


        Bots.update_one({"_id":bot_id},{"$inc":{"count_hev":+count}})
        ids = Hist.insert_one(post).inserted_id
        if Bots.find_one({"_id":bot_id})['first_bye'] == "":
            Bots.update_one({"_id": bot_id}, {"$set": {"first_bye": ids}})
        Bots.update_one({"_id": bot_id}, {"$set": {"last_bye": ids}})


    def postOperationSell(self, bot_id, sell_lvl, valute_par, count):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        Bots = db["Bots"]
        bot = Bots.find_one({"_id":bot_id})

        first_bye = Hist.find_one({"_id":ObjectId(bot['first_bye'])})
        price_first_bye  = first_bye['lvl']
        price_sell = sell_lvl
        profit = 100-((price_first_bye/price_sell)*100)

        post = {
            "lvl": sell_lvl,
            "valute_par": valute_par,
            "count": count,
            "type":"Продажа",
            "date":datetime.now(),
            "profit": profit,
            "bot_id":bot_id
        }

        Bots.update_one({"_id": bot_id}, {"$inc": {"count_hev": -count}})
        Bots.update_one({"_id": bot_id}, {"$set": {"first_bye": ""}})
        Bots.update_one({"_id": bot_id}, {"$inc": {"sum_invest":(bot['sum_invest']*(profit/100))}})
        Hist.insert_one(post)

    def postOperationOrgerBy(self, bye_lvl, valute_par, count,bot_id,orger_id):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        Bots = db["Bots"]

        post = {
            "lvl": bye_lvl,
            "valute_par": valute_par,
            "count": count,
            "type":"Ордер на закупку",
            "date":datetime.now(),
            "profit": 0,
            "bot_id": bot_id

        }

        Hist.insert_one(post)
        Bots.update_one({"_id": bot_id},{"$set":{"order":orger_id}})


    def setOrder(self,bot_id,status):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.update_one({"_id": bot_id}, {"$set": {"order": status}})

    def getAllHist(self):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        return Hist.find({})
