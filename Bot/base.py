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
            'next_check': next_check,
            'order': False,
            "count_hev": 0,  # записывать количество
            'last_bye': "",  # Записывать id последней покупки
            'triger': triger
        }

        return Bots.insert_one(post).inserted_id

    def delBot(self, id):
        db = self.classter["BinanceInvest"]
        Bots = db["Bots"]

        Bots.delete_one({'_id': ObjectId(id)})

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
        Bots.update_one({"_id": bot_id}, {"$set": {"last_bye": ids}})


    def postOperationSell(self, bot_id, sell_lvl, valute_par, count):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]
        Bots = db["Bots"]

        last_bye = Hist.find_one({"_id":ObjectId(Bots.find_one({"_id":bot_id})['last_bye'])})
        price_bye = last_bye['lvl']
        price_sell = sell_lvl

        post = {
            "lvl": sell_lvl,
            "valute_par": valute_par,
            "count": count,
            "type":"Продажа",
            "date":datetime.now(),
            "profit": 100-(price_bye/price_sell)*100,
            "bot_id":bot_id
        }

        Bots.update_one({"_id": bot_id}, {"$inc": {"count_hev": -count}})
        Hist.insert_one(post)

    def postOperationOrgerBy(self, bye_lvl, valute_par, count,bot_id):
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

        ids = Hist.insert_one(post)
        Bots.update_one({"_id": bot_id},{"$set":{"order":ids}})

    def getAllHist(self):
        db = self.classter["BinanceInvest"]
        Hist = db["Hist"]

        return Hist.find({})
