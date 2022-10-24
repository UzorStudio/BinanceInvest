#from binance.client import Client
import random

#client = Client("cIejKCqQQ0eIfte67cTjuZTRzU2dKCfqZg8071RJq8BIQsuvkhIZiFRChLDXvBuq",
#                "4z0NTs2PMcpBXok6CA8iNE9k005WfPULbAqQN2CGtSSPvPFHWIYXpEN0y2AFexu3")


#orders = client.get_all_orders(symbol='BNBBTC', limit=10)
#print(orders)

dollar = 10
i = 0
pr =[]
while dollar <= 1000:
    profit = random.randint(5,21)/100
    pr.append(profit)
    #profit = 0.21
    dollar = dollar+(dollar*profit)
    i +=1
    print(f"{dollar} {i} {profit}")

print(sum(pr)/len(pr))
#
#
#
#info = client.get_account()['balances']
#
#for i in info:
#    if float(i['free']) > 0:
#        print(i)