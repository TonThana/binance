import threading
import time
from binance.client import Client
import numpy as np
from secret.key import api_key, api_secret

client = Client(api_key=api_key,
                api_secret=api_secret)

start = []
volstart = []
current = []
diff = []


def callBTCPairPrice():
    current = []
    prices = client.get_all_tickers()
    BTC = "BTC"
    # test = []
    for item in prices:
        if (BTC in item['symbol']):
            refactor = {"name": item['symbol'],
                        "price": float(item['price'])}
            # print(refactor)
            current.append(refactor)
    for (index, item) in enumerate(current):

        percentageChange = np.round((item['price'] - start[index]['price'])
                                    * 100/start[index]['price'], 4)
        # print(item['name'], item['price'],index)
        if (percentageChange) > 4:
            # volume -
            currentVol = float(client.get_ticker(
                symbol=item['name'])['volume'])
            percentageVolChange = np.round((currentVol - volstart[index]['volume'])
                                           * 100/volstart[index]['volume'], 4)
            print(item['name'], percentageChange, percentageVolChange)

    print("----------------")


def initialiseBTCPairPrice():
    prices = client.get_all_tickers()
    BTC = "BTC"
    for item in prices:
        if (BTC in item['symbol']):
            refactor = {"name": item['symbol'],
                        "price": float(item['price'])}
            start.append(refactor)
    print("INITIALISE PRICES")


def initialiseBTCPairVolume():
    allInfo = client.get_ticker()
    BTC = "BTC"
    for item in allInfo:
        if (BTC in item['symbol']):
            refactor = {"name": item['symbol'],
                        "volume": float(item['volume'])}
            volstart.append(refactor)
    print("INITIALISE allInfo")


StartTime = time.time()


def action():
    callBTCPairPrice()


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()
        initialiseBTCPairPrice()
        initialiseBTCPairVolume()

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


# start action every 0.6s
inter = setInterval(5, action)
print('just after setInterval -> time : {:.1f}s'.format(time.time()-StartTime))

# will stop interval in 5s
t = threading.Timer(3600, inter.cancel)
t.start()
