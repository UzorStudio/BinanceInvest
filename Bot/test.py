import threading
from threading import Thread

def worker():
    print("w")

tr = Thread(target=worker, args=())
print()
tr.start()















#from binance.client import Client
#
#client = Client("cIejKCqQQ0eIfte67cTjuZTRzU2dKCfqZg8071RJq8BIQsuvkhIZiFRChLDXvBuq",
#                "4z0NTs2PMcpBXok6CA8iNE9k005WfPULbAqQN2CGtSSPvPFHWIYXpEN0y2AFexu3")
#
#info = client.get_account()['balances']
#
#for i in info:
#    if float(i['free']) > 0:
#        print(i)