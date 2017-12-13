import requests

def getUrl(timeframe, exchange, type):
    # Response with Section = "last"
    # [ 
    #   MTS, 
    #   OPEN, 
    #   CLOSE, 
    #   HIGH, 
    #   LOW, 
    #   VOLUME 
    # ]

    # Response with Section = "hist"
    # [
    #   [ MTS, OPEN, CLOSE, HIGH, LOW, VOLUME ], 
    #   ...
    # ]
    return 'https://api.bitfinex.com/v2/candles/trade:' + timeframe + ':' + exchange + '/' + type

def percentageVariation(start, end):
        return end/start    

params = {
    'limit': 10,
    # 'start': 1512481400000,
    # 'end': 1512491400000,
    'sort': -1
}
url = getUrl('12h', 'tBTCUSD', 'hist')

r = requests.get(url, params=params)

print('Total of candles: ' + str(len(r.json())))
# print(r.json())
for candle in r.json():
    if (candle[1] < candle[2]):
        print ('UP\t- ' + 'Variation: ' + str('%.8f' % percentageVariation(candle[1], candle[2])) + ';\t\tStart: ' + str('%.2f' % candle[1]) + ';\t\tEnd: ' + str('%.2f' % candle[2]))
    else:
        print ('Down\t- ' + 'Variation: ' + str('%.8f' % percentageVariation(candle[1], candle[2])) + ';\t\tStart: ' + str('%.2f' % candle[1]) + ';\t\tEnd: ' + str('%.2f' % candle[2]))
# print(r.json()[0])
# print(r.json()[len(r.json()) - 1])