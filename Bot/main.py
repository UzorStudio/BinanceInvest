import logging
import threading

from requests import ReadTimeout

import helpFunctions as hlp
from time import sleep

from binance.client import Client
from flask import Flask, render_template, request, redirect, session
import base
from datetime import datetime, timedelta
from threading import Thread
import bin_func

db = base.Base("mongodb://Roooasr:sedsaigUG12IHKJhihsifhaosf@mongodb:27017/")
#db = base.Base("localhost")
API_PATH = "conf.txt"

apis = open(API_PATH, "r").readlines()
print(apis)
client = Client(apis[0].replace("\n", ""),
                apis[1].replace("\n", ""),
                )
db.UpdateSymbolInfo(client)
db.UpdateTikers(client)
app = Flask(__name__)
app.secret_key = "mimoza1122"


def regSess(sesid):
    session["sesid"] = str(sesid)


def delSess():
    try:
        session.pop("sesid", None)
    except:
        pass


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":

        symbol = request.form["symbol"]
        if symbol != '':
            bots = db.getBotsBySymbol(symbol)
        else:
            bots = db.getAllBots()
        b = []

        info = client.get_account()['balances']
        balances = []

        for i in info:
            if float(i['free']) > 0:
                balances.append(i)

        for bot in bots:
            if len(str(bot['bye_lvl']).split('e')) > 1:
                bot['bye_lvl'] = format(float(bot['bye_lvl']), ".8f")
            if len(str(bot['sum_invest']).split('e')) > 1:
                bot['sum_invest'] = toFixed(bot['sum_invest'], 8)
            if len(str(bot['sell_lvl']).split('e')) > 1:
                bot['sell_lvl'] = format(float(bot['sell_lvl']), ".8f")
            if len(str(bot['earned']).split('e')) > 1:
                bot['earned'] = toFixed(bot['earned'], 8)
            if len(str(bot['spent']).split('e')) > 1:
                bot['spent'] = toFixed(bot['spent'], 8)
            if len(str(bot['cikle_profit']).split('e')) > 1:
                bot['cikle_profit'] = toFixed(bot['cikle_profit'], 8)
            if len(str(bot['total_profit']).split('e')) > 1:
                bot['total_profit'] = toFixed(bot['total_profit'], 8)
            if len(str(bot['triger_lvl']).split('e')) > 1:
                bot['triger_lvl'] = format(float(bot['triger_lvl']), ".8f")
            if len(str(bot['count_hev']).split('e')) > 1:
                bot['count_hev'] = format(float(bot['count_hev']), ".8f")

            b.append(
                {"bot": bot})

        return render_template("index.html", bo=b, par=db.openSymbol(), balance=balances)

    else:
        bots = db.getAllBots()
        b = []

        info = client.get_account()['balances']
        balances = []

        for i in info:
            if float(i['free']) > 0:
                balances.append(i)

        for bot in bots:
            if len(str(bot['bye_lvl']).split('e')) > 1:
                bot['bye_lvl'] = format(float(bot['bye_lvl']), ".8f")
            if len(str(bot['sum_invest']).split('e')) > 1:
                bot['sum_invest'] = toFixed(bot['sum_invest'], 8)
            if len(str(bot['sell_lvl']).split('e')) > 1:
                bot['sell_lvl'] = format(float(bot['sell_lvl']), ".8f")
            if len(str(bot['earned']).split('e')) > 1:
                bot['earned'] = toFixed(bot['earned'], 8)
            if len(str(bot['spent']).split('e')) > 1:
                bot['spent'] = toFixed(bot['spent'], 8)
            if len(str(bot['cikle_profit']).split('e')) > 1:
                bot['cikle_profit'] = toFixed(bot['cikle_profit'], 2)
            if len(str(bot['total_profit']).split('e')) > 1:
                bot['total_profit'] = toFixed(bot['total_profit'], 2)
            if len(str(bot['triger_lvl']).split('e')) > 1:
                bot['triger_lvl'] = format(float(bot['triger_lvl']), ".8f")
            if len(str(bot['count_hev']).split('e')) > 1:
                bot['count_hev'] = format(float(bot['count_hev']), ".8f")
            if len(str(bot['total_sum_invest']).split('e')) > 1:
                bot['total_sum_invest'] = toFixed(bot['total_sum_invest'], 8)

            b.append(
                {"bot": bot})

        return render_template("index.html", bo=b, par=db.openSymbol(), balance=balances)


@app.route("/archive", methods=["POST", "GET"])
def archive():
    if request.method == "POST":

        email = request.form["email"]

    else:
        bots = db.getAllBots()
        b = []
        for bot in bots:
            b.append(
                {"bot": bot, "price": format(float(client.get_avg_price(symbol=bot['valute_par'])['price']), ".8f")})

        return render_template("archive.html", bo=b)


@app.route("/settings", methods=["POST", "GET"])
def settings():
    if request.method == "POST":

        api_key = request.form["api_key"]
        api_secret = request.form["api_secret"]
        open(API_PATH, "w").write(f"{api_key}\n{api_secret}\n")
        api = open(API_PATH, "r").readlines()

        return render_template("settings.html", api=api)


    else:
        api = open(API_PATH, "r").readlines()
        try:
            print(client.get_account())
        except:
            print("err")
        return render_template("settings.html", api=api)


@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        triger_lvl = None
        trigger = False

        valute_par = request.form["valute_par"]
        name = request.form["name"]
        sum_invest = request.form["sum_invest"]
        bye_lvl = request.form["bye_lvl"]
        sell_lvl = request.form["sell_lvl"]
        try:
            if request.form["triger"]:
                triger_lvl = request.form["triger_lvl"]
                trigger = True
        except:
            triger_lvl = 0
        valuecheck = request.form["valuecheck"]
        check_time = request.form["check_time"]
        total_sum_invest = request.form["total_sum_invest"]

        ids = db.regBot(valute_par=valute_par,
                        name=name,
                        sum_invest=sum_invest,
                        bye_lvl=bye_lvl,
                        sell_lvl=sell_lvl,
                        triger_lvl=triger_lvl,
                        valuecheck=valuecheck,
                        check_time=check_time,
                        triger=trigger,
                        total_sum_invest=total_sum_invest)
        return redirect('/')
    else:

        info = client.get_account()['balances']
        balances = []

        for i in info:
            if float(i['free']) > 0:
                balances.append(i)

        tck = []
        for t in db.getAllTickers():
            if len(str(hlp.getMinInv(t['symbol'])).split('e')) > 1:
                tck.append({"minimum": format(float(hlp.getMinInv(t['symbol'])), ".8f"), "par": t})
            else:
                tck.append({"minimum": hlp.getMinInv(t['symbol']), "par": t})

        return render_template("createbot.html", coin=tck, balance=balances)


@app.route("/delbot/<string:id>", methods=["POST", "GET"])
def delbot(id):
    if request.method == "POST":
        pass
    else:
        db.delBot(id)
        return redirect('/')


@app.route("/returnbot/<string:id>", methods=["POST", "GET"])
def returnbot(id):
    if request.method == "POST":
        pass
    else:
        db.returnBot(id)
        return redirect('/archive')


@app.route("/botsetings/<string:id>", methods=["POST", "GET"])
def botsetings(id):
    if request.method == "POST":
        triger_lvl = None
        trigger = False

        sum_invest = request.form["sum_invest"]
        base_total_sum_invest = request.form["base_total_sum_invest"]
        bye_lvl = request.form["bye_lvl"]
        sell_lvl = request.form["sell_lvl"]
        try:
            if request.form["triger"]:
                triger_lvl = request.form["triger_lvl"]
                trigger = True
        except:
            triger_lvl = 0
        valuecheck = request.form["valuecheck"]
        check_time = request.form["check_time"]

        db.reloadBot(id=id,
                     sum_invest=sum_invest,
                     bye_lvl=bye_lvl,
                     sell_lvl=sell_lvl,
                     triger_lvl=triger_lvl,
                     valuecheck=valuecheck,
                     check_time=check_time,
                     triger=trigger,
                     base_total_sum_invest=base_total_sum_invest)
        return redirect(f'/botsetings/{str(id)}')
    else:
        bo = db.getBot(id)

        if len(str(bo['bye_lvl']).split('e')) > 1:
            bo['bye_lvl'] = format(float(bo['bye_lvl']), ".8f")
        if len(str(bo['sum_invest']).split('e')) > 1:
            bo['sum_invest'] = format(float(bo['sum_invest']), ".8f")
        if len(str(bo['sell_lvl']).split('e')) > 1:
            bo['sell_lvl'] = format(float(bo['sell_lvl']), ".8f")
        if len(str(bo['triger_lvl']).split('e')) > 1:
            bo['triger_lvl'] = format(float(bo['triger_lvl']), ".8f")
        if len(str(bo['count_hev']).split('e')) > 1:
            bo['count_hev'] = format(float(bo['count_hev']), ".8f")
        if len(str(bo['total_sum_invest']).split('e')) > 1:
            bo['total_sum_invest'] = toFixed(bo['total_sum_invest'], 8)

        return render_template("botsetings.html", bot=bo)


@app.route("/message", methods=["POST", "GET"])
def message():
    if request.method == "POST":
        dateset = db.openHistDate()
        print(request.form)
        if 'calendar' in request.form and 'proc' in request.form:
            if request.form['calendar'] != '':
                date = request.form["calendar"]
                history = db.getHistByDay(date)
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)
                return render_template("message.html", hist=hist, d=dateset)
            if request.form['proc'] != '':
                proc = request.form["proc"]
                history = db.getHistByProc(int(proc))
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)

                return render_template("message.html", hist=hist, d=db.openHistByProc(proc))
            if request.form['proc'] != '' and request.form['calendar'] != '':
                proc = request.form["proc"]
                date = request.form["calendar"]
                history = db.getHistByProcDay(int(proc), date)
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)

                return render_template("message.html", hist=hist, d=dateset)
        if 'dataopen' in request.form:
            date = request.form["dataopen"]
            history = db.getHistByDay(date=date)
            hist = []
            for h in history:
                h['lvl'] = format(float(h['lvl']), ".8f")
                h['count'] = format(float(h['count']), ".8f")
                hist.append(h)
            return render_template("message.html", hist=hist, d=dateset)

        else:
            return redirect('/message')


    else:
        dateset = db.openHistDate()
        history = db.getHistToDey()
        hist = []

        for h in history:
            h['lvl'] = format(float(h['lvl']), ".8f")
            h['count'] = format(float(h['count']), ".8f")
            hist.append(h)
        return render_template("message.html", hist=hist, d=dateset)


@app.route("/message/<string:id>", methods=["POST", "GET"])
def messagebot(id):
    if request.method == "POST":
        print(request.form)
        da = db.openHistBotDate(id)
        if 'calendar' in request.form and 'proc' in request.form:
            if request.form['calendar'] != '':
                date = request.form["calendar"]
                history = db.getHistByBotIdDate(date=date, id=id)
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)
                return render_template("message.html", hist=hist, d=da)

            if request.form['proc'] != '':
                proc = request.form["proc"]
                history = db.getHistByProcBot(int(proc), id)
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)

                return render_template("message.html", hist=hist, d=da)

            if request.form['proc'] != '' and request.form['calendar'] != '':
                proc = request.form["proc"]
                date = request.form["calendar"]
                history = db.getHistByProcDayBot(prof=int(proc), date=date, id=id)
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)

                return render_template("message.html", hist=hist, d=da)
            else:
                return render_template("err")
        if 'dataopen' in request.form:
            date = request.form["dataopen"]
            history = db.getHistByBotIdDate(date=date, id=id)
            hist = []
            print(date)

            for h in history:
                h['lvl'] = format(float(h['lvl']), ".8f")
                h['count'] = format(float(h['count']), ".8f")
                hist.append(h)
            return render_template("message.html", hist=hist, d=da)
    else:
        date = db.openHistBotDate(id)
        history = db.getHistByBotId(id)
        hist = []

        for h in history:
            h['lvl'] = format(float(h['lvl']), ".8f")
            h['count'] = format(float(h['count']), ".8f")
            hist.append(h)

        return render_template("message.html", hist=hist, d=date)

@app.route("/zeros", methods=["POST","GET"])
def zeros():
    if request.method == "POST":
        pass
    else:
        db.ZeroBot()
        return redirect('/')

def checkOrers(bot,price):
    for order_bot in db.getOrdersByeBot(bot['_id']):
        order = client.get_order(
            symbol=bot['valute_par'],
            orderId=str(order_bot))
        if order["status"] == 'FILLED' and order["side"] == 'BUY':
            db.postOperationBye(bot_id=bot['_id'],
                                order=order,
                                valute_par=bot['valute_par'],
                                count=float(order['executedQty']),
                                spent=float(order['cummulativeQuoteQty']),
                                bye_lvl=order['price'])
            ##  Добавил
            bot = db.getBot(bot["_id"])
            logging.info(f"___sell post bye: {bot}")
            if bot['count_hev'] > 0:
                total_balance = client.get_account()['balances']
                logging.info(f"spent_true: {bot['spent_true']}")
                order = bin_func.Sell(bot['valute_par'], inv_sum=bot['count_hev'],total_balance = total_balance, client=client, price=bot['sell_lvl'])
                if order and float(order['bye']['count']) > 0:
                    print(bot['spent_true'])
                    db.SellForBot(bot_id=bot['_id'], order=order, spent=bot['spent_true'])

        cnsl = hlp.cansle_order(order, client,bot['triger_lvl'],price)
        if cnsl != 0:
            print(f"cnsl: {bot['_id']} ")
            print(f"cnsl status: {cnsl}")
            db.setTriger(bot["_id"], False)
            db.returnCountHev(bot["_id"], cnsl)
            db.dropLastPriceForPrice(bot["_id"], cnsl["price"])
            db.dropOrderId(bot["_id"], cnsl)

    for order_bot in db.getOrdersSellBot(bot['_id']):
        order = client.get_order(
            symbol=bot['valute_par'],
            orderId=str(order_bot['id']))
        if order["status"] == 'FILLED' and order["side"] == 'SELL':
            db.setTriger(bot["_id"], False)
            ern = db.postOperationSell(bot_id=bot['_id'],
                                 order=order,
                                 valute_par=bot['valute_par'],
                                 count=order['cummulativeQuoteQty'],
                                 sell_lvl=order['price'],
                                 spent=order_bot['spents'])
            client.transfer_spot_to_margin(asset=hlp.split_symbol(bot['valute_par'])['quoteAsset'], amount=toFixed(ern,8))
            print(f"sell in paarsers {bot['_id']}")
            db.dropLastPrice(bot["_id"])
        if order["status"] == 'CANCELED' and order["side"] == 'SELL':
            db.cancelOrderSell(origQty=order['origQty'],orderId=order['orderId'],bot_id=bot["_id"])
        if order["status"] == 'CANCELED' and order["side"] == 'BUY':
            db.cancelOrderBye(order=order,bot_id=bot["_id"])


def sellUpBot(bot):
    price = float(client.get_avg_price(symbol=bot['valute_par'])['price'])
    for order_bot in db.getOrdersSellBot(bot['_id']):
        order = client.get_order(
            symbol=bot['valute_par'],
            orderId=str(order_bot['id']))
        if order["side"] == 'SELL':
            if "updateTime" in order:
                time_order = datetime.fromtimestamp(int(order['updateTime']) / 1000)
                if time_order + timedelta(hours=1) < datetime.now() and order['status'] == 'NEW':
                    for ord in bot['orders_sell']:
                        if max(ord["be_bye"]) < price:

                            orderforsell = client.get_order(
                                symbol=bot['valute_par'],
                                orderId=str(ord['id']))
                            db.cancelOrderSell(bot_id=bot['_id'],orderId=ord['id'],origQty=orderforsell['origQty'])
                            client.cancel_order(
                                symbol=bot['valute_par'],
                                orderId=str(ord['id']))
                            bot = db.getBot(bot["_id"])
                            logging.info(f"___sell post cansle post 1 hour: {bot}")



                            if bot['count_hev'] > 0:
                                total_balance = client.get_account()['balances']
                                logging.info(f"spent_true: {bot['spent_true']}")
                                order = bin_func.Sell(bot['valute_par'], inv_sum=bot['count_hev'],
                                                      total_balance=total_balance, client=client, price=price)
                                if order and float(order['bye']['count']) > 0:
                                    print(bot['spent_true'])
                                    db.SellForBot(bot_id=bot['_id'], order=order, spent=bot['spent_true'])


            else:
                pass



def belayOrder(bot,price):
    for order_bot in db.getOrdersSellBot(bot['_id']):
        order = client.get_order(
            symbol=bot['valute_par'],
            orderId=str(order_bot['id']))
        if order["side"] == 'SELL':
            if "updateTime" in order:
                time_order = datetime.fromtimestamp(int(order['updateTime']) / 1000)
                if time_order + timedelta(hours=24) < datetime.now() and order['status'] == 'NEW':
                    for ord in bot['orders_sell']:
                        if min(ord["be_bye"]) > price:
                            if 1-(price/min(ord["be_bye"])) > 0.02:
                                orderforsell = client.get_order(
                                    symbol=bot['valute_par'],
                                    orderId=str(ord['id']))
                                db.cancelOrderSell(bot_id=bot['_id'], orderId=ord['id'],
                                                   origQty=orderforsell['origQty'])
                                client.cancel_order(
                                    symbol=bot['valute_par'],
                                    orderId=str(ord['id']))
                                bot = db.getBot(bot["_id"])

                                if bot['count_hev'] > 0:
                                    total_balance = client.get_account()['balances']
                                    logging.info(f"spent_true: {bot['spent_true']}")
                                    order = bin_func.Sell(bot['valute_par'], inv_sum=bot['count_hev'],
                                                          total_balance=total_balance, client=client, price=price)
                                    if order and float(order['bye']['count']) > 0:
                                        print(bot['spent_true'])
                                        db.SellForBot(bot_id=bot['_id'], order=order, spent=bot['spent_true'])


def worker():
    print("tr start")

    while True:
        bots = db.getAllBots()
        logging.info(f"Check time {datetime.now()}")
        for bot in bots:

            if bot['next_check'] <= datetime.now() and bot['not_archive']:
                datecleck = datetime.now().time().second
                total_balance = client.get_account()['balances']
                db.botNextCheck(bot['_id'])
                price = float(client.get_avg_price(symbol=bot['valute_par'])['price'])
                logging.info(f"{bot['name']} {bot['_id']} Now price: {price} Bye lvl: {bot['bye_lvl']}")
                checkOrers(bot, price)
                bot = db.getBot(bot["_id"])

                if price <= bot['bye_lvl'] and bot["total_sum_invest"] >= hlp.getMinInv(
                        bot['valute_par']) and price not in bot['last_price']:  # BYE
                    order = bin_func.Bye(symb=bot['valute_par'], client=client, inv_sum=bot['sum_invest'],
                                         balance=bot['total_sum_invest'],price=price,total_balance=total_balance)

                    if order:
                        db.setLastPrice(bot["_id"], price)
                        db.ByeForBot(bot_id=bot['_id'],
                                     order=order, spent=float(order["sell"]["count"]))
                        bot = db.getBot(bot["_id"])
                    else:
                        logging.error(
                            f"NONE BALANCE {bot['name']} {bot['_id']} Now price: {price} Bye lvl: {bot['bye_lvl']}")

                elif price >= bot['sell_lvl'] and bot['count_hev'] > 0:  # SELL

                    order = bin_func.Sell(bot['valute_par'], inv_sum=bot['count_hev'], client=client,price=price,total_balance=total_balance)
                    if order and float(order['bye']['count']) > 0:
                        bot = db.getBot(bot["_id"])
                        db.SellForBot(bot_id=bot['_id'], order=order, spent=bot['spent_true'])



                if price <= bot['triger_lvl'] and bot[
                    "total_sum_invest"] >= hlp.getMinInv(bot['valute_par']) and price not in bot['last_price']:
                    order = bin_func.BuyOrder(symb=bot['valute_par'], client=client, inv_sum=bot['sum_invest'],
                                              balance=bot['total_sum_invest'], price=bot["bye_lvl"],total_balance=total_balance)

                    if order:
                        db.setLastPrice(bot["_id"], price)
                        db.ByeForBot(bot_id=bot['_id'],
                                     order=order, spent=float(order["sell"]["count"]))
                bot = db.getBot(bot["_id"])
                sellUpBot(bot)
                bot = db.getBot(bot["_id"])
                belayOrder(bot=bot,price=price)
                logging.info(f"[[[[[time loss: {datecleck - datetime.now().time().second}]]]]]")

        sleep(30)


def start():
    try:
        if threading.enumerate():
            tr = Thread(target=worker, args=(), name="test")
            tr.start()
        else:
            print(f"tr err thr count:{len(threading.enumerate())}")
    except ReadTimeout as e:
        print(f"ReadTimeout {e.args}")
        sleep(15)
        start()


if __name__ == "__main__":
    start()
    app.run(debug=False, host="0.0.0.0", port=5000)
