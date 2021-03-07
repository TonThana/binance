import threading
import time
from binance.client import Client
import numpy as np
from datetime import datetime
from secret.key import api_key, api_secret
import pickle

client = Client(api_key=api_key,
                api_secret=api_secret)


def callPrice(pair='', start=[], volstart=[]):

    current = []
    prices = client.get_all_tickers()
    for item in prices:
        if (pair in item['symbol']):
            refactor = {"name": item['symbol'],
                        "price": float(item['price'])}
            # print(refactor)
            current.append(refactor)

    for (index, item) in enumerate(current):

        percentageChange = np.round(
            (item['price'] - start[index]['price']) * 100/start[index]['price'], 4)
        # print(item['name'], item['price'],index)

        # more than 2% increase
        if (percentageChange) > 2:
            # if price increase more than x percent - volume?
            currentVol = float(client.get_ticker(
                symbol=item['name'])['volume'])
            percentageVolChange = np.round((currentVol - volstart[index]['volume'])
                                           * 100/volstart[index]['volume'], 4)
            # must have positive vol change 5% threshold
            if percentageVolChange > 5:
                print(item['name'], percentageChange, percentageVolChange)

    print("----------------")


def initialisePrice(pair='', useHistory=False):
    start = []
    if (useHistory == True):
        start = pickle.load(open('./price175007032021.p', 'rb'))
    else:
        prices = client.get_all_tickers()
        for item in prices:
            if (pair in item['symbol']):
                refactor = {"name": item['symbol'],
                            "price": float(item['price'])}
                start.append(refactor)
        # save as history
        pickle.dump(start, open("./price175007032021.p", "wb"))
    return start


def initialiseVolume(pair='', useHistory=False):
    volstart = []
    if (useHistory == True):
        volstart = pickle.load(open('./others170507032021.p', 'rb'))
    else:
        allInfo = client.get_ticker()
        for item in allInfo:
            if (pair in item['symbol']):
                refactor = {"name": item['symbol'],
                            "volume": float(item['volume'])}
                volstart.append(refactor)
        print("INITIALISE ALL INFO")
        # save as history
        pickle.dump(volstart, open("./others175007032021.p", "wb"))
    return volstart


StartTime = time.time()


def action():
    callPrice(pair="BTC")


class setInterval:
    def __init__(self, interval, action):
        print("initialise")
        self.interval = interval
        self.callPrice = callPrice
        self.stopEvent = threading.Event()
        self.useHistory = False
        thread = threading.Thread(target=self.__setInterval)
        thread.start()
        self.start = initialisePrice(pair="BTC", useHistory=self.useHistory)
        self.volstart = initialiseVolume(
            pair="BTC", useHistory=self.useHistory)
        startTime = datetime.now()
        startTime = startTime.strftime("%H:%M:%S")

        print("start time: ", startTime)

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.interval
            self.callPrice(pair="BTC", start=self.start,
                           volstart=self.volstart)

    def cancel(self):
        self.stopEvent.set()


# start action every 0.6s
inter = setInterval(5, action)
print('just after setInterval -> time : {:.1f}s'.format(time.time()-StartTime))

# will stop interval in 5s
t = threading.Timer(3600, inter.cancel)
t.start()


# TERMINOLOGY
# Volume: how much (of the coin) has been traded in the last 24 hours

# Circulating supply: how much of the coin currently exists

# Market Cap: Market capitalization; price of coin * circulating supply = Market Cap. That is to say, how much is the total net worth or value of the coin.
