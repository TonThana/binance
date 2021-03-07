# from binance.client import Client
# from secret.key import api_key, api_secret

# client = Client(api_key=api_key,
#                 api_secret=api_secret)


# def getInfo(pair=''):
#     allInfo = client.get_ticker()
#     print(allInfo[0])


# getInfo()

# # : '0.03249200', 'lastPrice': '0.03310800', 'lastQty': '0.90000000', 'bidPrice': '0.03310700', 'bidQty': '0.35200000', 'askPrice': '0.03310800', 'askQty': '31.92200000', 'openPrice': '0.03249200', 'highPrice': '0.03450000', 'lowPrice': '0.03211300', 'volume': '412041.99200000', 'quoteVolume': '13729.68626254', 'openTime': 1615021568178, 'closeTime': 1615107968178, 'firstId': 239371275, 'lastId': 239758420, 'count': 387146}

import pickle


prices = pickle.load(open('price170507032021.p', 'rb'))
print(prices)
