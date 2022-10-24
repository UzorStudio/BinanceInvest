import threading
from time import sleep

from binance.client import Client
from binance.enums import SIDE_BUY, TIME_IN_FORCE_GTC, ORDER_TYPE_LIMIT
from flask import Flask, render_template, request, redirect, session
import base
from datetime import datetime
from threading import Thread

apis = open("Bot/conf.txt","r").readlines()
print(apis)
#db = base.Base("mongodb://Roooasr:sedsaigUG12IHKJhihsifhaosf@mongodb:27017/")
db = base.Base("localhost")

client = Client(apis[0].replace("\n",""),
                apis[1].replace("\n",""))

app = Flask(__name__)
app.secret_key = "mimoza1122"


def regSess(sesid):
    session["sesid"] = str(sesid)


def delSess():
    try:
        session.pop("sesid", None)
    except:
        pass


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":

        email = request.form["email"]

    else:
        bots = db.getAllBots()
        b = []
        for bot in bots:
            b.append({"bot":bot,"price":float(client.get_avg_price(symbol=bot['valute_par'])['price'])})

        return render_template("index.html", bo=b)


@app.route("/archive", methods=["POST", "GET"])
def archive():
    if request.method == "POST":

        email = request.form["email"]

    else:
        bots = db.getAllBots()
        b = []
        for bot in bots:
            b.append({"bot":bot,"price":float(client.get_avg_price(symbol=bot['valute_par'])['price'])})

        return render_template("archive.html", bo=b)

@app.route("/settings", methods=["POST", "GET"])
def settings():
    if request.method == "POST":

        email = request.form["email"]

    else:

        return render_template("settings.html")


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

        return render_template("createbot.html",coin=client.get_all_tickers(),balance= balances)

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

        email = request.form["email"]

    else:

        return render_template("message.html",hist=db.getAllHist())




def worker():
    print("tr start")

    while True:
        bots  = db.getAllBots()

        for bot in bots:
            print(datetime.now())
            if bot['next_check'] <= datetime.now() and bot['not_archive']:
                db.botNextCheck(bot['_id'])

                price = float(client.get_avg_price(symbol=bot['valute_par'])['price'])
                print(f"{price} {bot['bye_lvl']}")

                if price <= bot['bye_lvl']: # BYE
                    count = bot['sum_invest'] * price

                    #order = client.order_market_buy(
                    #    symbol=bot['valute_par'],
                    #    quantity=bot['sum_invest'])

                    db.postOperationBye(bye_lvl=price,valute_par=bot['valute_par'],count=count,bot_id=bot['_id'])
                elif price >= bot['sell_lvl'] and bot['count_hev'] > 0: # SELL
                    count = bot['count_hev']

                    #order = client.order_market_sell(
                    #    symbol=bot['valute_par'],
                    #    quantity=count)

                    db.postOperationSell(sell_lvl=price,valute_par=bot['valute_par'],count=count,bot_id=bot['_id'])



                if price >= bot['triger_lvl'] and bot["order"] == False:

                    #order = client.create_order(
                    #    symbol=bot['valute_par'],
                    #    side=SIDE_BUY,
                    #    type=ORDER_TYPE_LIMIT,
                    #    timeInForce=TIME_IN_FORCE_GTC,
                    #    quantity=bot['sum_invest'],
                    #    price= bot['bye_lvl'])

                    db.postOperationOrgerBy(bye_lvl=bot['bye_lvl'],valute_par=bot['valute_par'],count=bot['sum_invest'],bot_id=bot['_id'],orger_id="order['orderId']")

                for ord in client.get_all_orders(symbol=bot['valute_par'], limit=10):
                    if ord['status'] != 'NEW':
                        db.setOrder(bot["_id"],False)
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
