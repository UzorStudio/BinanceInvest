import logging
import threading
import helpFunctions as hlp
from time import sleep

from binance.client import Client
from binance.enums import SIDE_BUY, TIME_IN_FORCE_GTC, ORDER_TYPE_LIMIT, SIDE_SELL
from flask import Flask, render_template, request, redirect, session
import base
from datetime import datetime
from threading import Thread

from Bot import bin_func

db = base.Base("mongodb://Roooasr:sedsaigUG12IHKJhihsifhaosf@mongodb:27017/")
#db = base.Base("localhost")
API_PATH = "Bot/conf.txt"

apis = open(API_PATH,"r").readlines()
print(apis)
client = Client(apis[0].replace("\n",""),
                apis[1].replace("\n",""),
                testnet=True)

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

        bots = db.getBotsBySymbol(symbol)
        b = []

        info = client.get_account()['balances']
        balances = []

        for i in info:
            if float(i['free']) > 0:
                balances.append(i)

        for bot in bots:
            razn = 0
            razn_sell = 0
            price = float(client.get_avg_price(symbol=bot['valute_par'])['price'])
            if len(str(bot['bye_lvl']).split('e')) > 1:
                bot['bye_lvl'] = format(float(bot['bye_lvl']), ".8f")
            if len(str(bot['sum_invest']).split('e')) > 1:
                bot['sum_invest'] = format(float(bot['sum_invest']), ".8f")
            if len(str(bot['sell_lvl']).split('e')) > 1:
                bot['sell_lvl'] = format(float(bot['bye_lvl']), ".8f")
            if len(str(bot['triger_lvl']).split('e')) > 1:
                bot['triger_lvl'] = format(float(bot['sell_lvl']), ".8f")
            if len(str(bot['count_hev']).split('e')) > 1:
                bot['count_hev'] = format(float(bot['count_hev']), ".8f")
            if len(str(price).split('e')) > 1:
                price = format(float(price), ".8f")
            if bot['bye_lvl'] < price:
                razn = 100*(1-float(bot['bye_lvl'])/float(price))
            if bot['bye_lvl'] > price:
                razn = 100 * (1 - float(price)/float(bot['bye_lvl']))
            if bot['sell_lvl'] < price:
                razn_sell = 100*(1-float(bot['sell_lvl'])/float(price))
            if bot['sell_lvl'] > price:
                razn_sell = 100 * (1 - float(price)/float(bot['sell_lvl']))

            b.append({"bot": bot, "price": price, "razn": toFixed(razn,2),"razn_sell":toFixed(razn_sell,2)})

        return render_template("index.html", bo=b, par=db.openSymbol(),balance = balances)

    else:
        bots = db.getAllBots()
        b = []

        info = client.get_account()['balances']
        balances = []

        for i in info:
            if float(i['free']) > 0:
                balances.append(i)

        for bot in bots:
            razn = 0
            price = float(client.get_avg_price(symbol=bot['valute_par'])['price'])
            if len(str(bot['bye_lvl']).split('e')) > 1:
                bot['bye_lvl'] = format(float(bot['bye_lvl']), ".8f")
            if len(str(bot['sum_invest']).split('e')) > 1:
                bot['sum_invest'] = format(float(bot['sum_invest']), ".8f")
            if len(str(bot['sell_lvl']).split('e')) > 1:
                bot['sell_lvl'] = format(float(bot['bye_lvl']), ".8f")
            if len(str(bot['triger_lvl']).split('e')) > 1:
                bot['triger_lvl'] = format(float(bot['sell_lvl']), ".8f")
            if len(str(bot['count_hev']).split('e')) > 1:
                bot['count_hev'] = format(float(bot['count_hev']), ".8f")
            if len(str(price).split('e')) > 1:
                price = format(float(price), ".8f")
            if bot['bye_lvl'] < price:
                razn = 100 * (1 - float(bot['bye_lvl']) / float(price))
            if bot['bye_lvl'] > price:
                razn = 100 * (1 - float(price) / float(bot['bye_lvl']))
            b.append({"bot": bot, "price": price, "razn": toFixed(razn,2)})


        return render_template("index.html", bo=b,par=db.openSymbol(),balance = balances)


@app.route("/archive", methods=["POST", "GET"])
def archive():
    if request.method == "POST":

        email = request.form["email"]

    else:
        bots = db.getAllBots()
        b = []
        for bot in bots:
            b.append({"bot":bot,"price":format(float(client.get_avg_price(symbol=bot['valute_par'])['price']),".8f")})

        return render_template("archive.html", bo=b)

@app.route("/settings", methods=["POST", "GET"])
def settings():
    if request.method == "POST":

        api_key = request.form["api_key"]
        api_secret = request.form["api_secret"]
        open(API_PATH,"w").write(f"{api_key}\n{api_secret}\n")
        api = open(API_PATH,"r").readlines()
        

        return render_template("settings.html",api=api)


    else:
        api = open(API_PATH, "r").readlines()
        try:
            print(client.get_account())
        except:
            print("err")
        return render_template("settings.html",api=api)


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

        ids = db.regBot(valute_par=valute_par,
                        name=name,
                        sum_invest=sum_invest,
                        bye_lvl=bye_lvl,
                        sell_lvl=sell_lvl,
                        triger_lvl=triger_lvl,
                        valuecheck=valuecheck,
                        check_time=check_time,
                        triger=trigger)
        return redirect(f'/botsetings/{str(ids)}')
    else:

        info = client.get_account()['balances']
        balances=[]

        for i in info:
            if float(i['free']) > 0:
                balances.append(i)

        tck = []
        for t in client.get_all_tickers():
            if len(str(hlp.getMinInv_test(t['symbol'])).split('e')) > 1:
                tck.append({"minimum": format(float(hlp.getMinInv_test(t['symbol'])), ".8f"), "par": t})
            else:
                tck.append({"minimum": hlp.getMinInv_test(t['symbol']), "par": t})

        return render_template("createbot.html",coin=tck,balance= balances)

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
                     triger=trigger)
        return redirect(f'/botsetings/{str(id)}')
    else:
        return render_template("botsetings.html", bot=db.getBot(id))


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
                return render_template("message.html", hist=hist,d =dateset)
            if request.form['proc'] != '':
                proc = request.form["proc"]
                history = db.getHistByProc(int(proc))
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)

                return render_template("message.html", hist=hist ,d =db.openHistByProc(proc))
            if request.form['proc'] != '' and request.form['calendar'] != '':
                proc = request.form["proc"]
                date = request.form["calendar"]
                history = db.getHistByProcDay(int(proc),date)
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)

                return render_template("message.html", hist=hist ,d =dateset)
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
        return render_template("message.html",hist=hist,d =dateset)


@app.route("/message/<string:id>", methods=["POST", "GET"])
def messagebot(id):
    if request.method == "POST":
        print(request.form)
        da = db.openHistBotDate(id)
        if 'calendar' in request.form and 'proc' in request.form:
            if request.form['calendar'] != '':
                date = request.form["calendar"]
                history = db.getHistByBotIdDate(date=date,id=id)
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)
                return render_template("message.html", hist=hist, d=da)

            if request.form['proc'] != '':
                proc = request.form["proc"]
                history = db.getHistByProcBot(int(proc),id)
                hist = []

                for h in history:
                    h['lvl'] = format(float(h['lvl']), ".8f")
                    h['count'] = format(float(h['count']), ".8f")
                    hist.append(h)

                return render_template("message.html", hist=hist, d=da)

            if request.form['proc'] != '' and request.form['calendar'] != '':
                proc = request.form["proc"]
                date = request.form["calendar"]
                history = db.getHistByProcDayBot(prof=int(proc), date=date,id=id)
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

        return render_template("message.html", hist=hist,d=date)
def worker():
    print("tr start")

    while True:
        bots  = db.getAllBots()
        logging.info(f"Check time {datetime.now()}")
        for bot in bots:

            if bot['next_check'] <= datetime.now() and bot['not_archive']:
                db.botNextCheck(bot['_id'])

                price = float(client.get_avg_price(symbol=bot['valute_par'])['price'])
                logging.info(f"{bot['name']} {bot['_id']} Now price: {price} Bye lvl: {bot['bye_lvl']}")

                if price <= bot['bye_lvl']: # BYE
                    order = bin_func.Bye(symb=bot['valute_par'],client=client,inv_sum=bot['sum_invest'])

                    if order:
                        db.postOperationBye(bye_lvl=price, valute_par=bot['valute_par'], count=float(order["bye"]["count"]), bot_id=bot['_id'],
                                             order=order,spent=float(order["sell"]["count"]))
                    else:
                        logging.error(f"NONE BALANCE {bot['name']} {bot['_id']} Now price: {price} Bye lvl: {bot['bye_lvl']}")

                elif price >= bot['sell_lvl'] and bot['count_hev'] > 0: # SELL

                    order = bin_func.Sell(bot['valute_par'],inv_sum=bot['count_hev'],client=client)
                    db.postOperationSell(sell_lvl=price,valute_par=bot['valute_par'],count=order['sell']['count'],bot_id=bot['_id'],order=order)



                if price >= bot['triger_lvl'] and bot["order"] == False:

                    order = bin_func.BuyOrder(symb=bot['valute_par'],
                                      inv_sum=bot['sum_invest'],
                                      priceb=bot['bye_lvl'],
                                      client=client)

                    db.postOperationOrgerBy(bye_lvl=bot['bye_lvl'],valute_par=bot['valute_par'],count=bot['sum_invest'],bot_id=bot['_id'],orger_id=order['order']['orderId'],orger=order)
                d = db.getOrderId(bot["_id"])
                if d !=0:
                    if bin_func.check_order(symb=bot['valute_par'],client=client,ordId=d["order"]["orderId"])['status'] == "FILLED":
                        db.postOperationBye(bye_lvl=price, valute_par=bot['valute_par'], count=bot['sum_invest'],
                                            bot_id=bot['_id'],
                                            order=d, spent=d["bye"]["count"])
                        db.setOrder(bot["_id"],False,0)
        sleep(30)


def start():

    if threading.enumerate():
        tr = Thread(target=worker, args=(), name="test")
        tr.start()
    else:
        print(f"tr err thr count:{len(threading.enumerate())}")




if __name__ == "__main__":

    start()
    app.run(debug=False, host="0.0.0.0", port=5000)


