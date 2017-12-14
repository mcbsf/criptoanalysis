import calendar

class Candle(object):
    timestamp = 0
    open_price = 0
    close_price = 0
    higher_price = 0
    lower_price = 0
    volume = 0
    percentage_variation = 0

    def __init__(self, timestamp, open_price, close_price, higher_price, lower_price, volume):
        self.timestamp = timestamp
        self.open_price = open_price
        self.close_price = close_price
        self.higher_price = higher_price
        self.lower_price = lower_price
        self.volume = volume
        self.percentage_variation = open_price/close_price 

    @property
    def seconds_timestamp(self):
        return str(self.timestamp)[0:-3]


class CoinChart(object):
    candles_timeframe = '12h'
    start_date = 0  # A datetime.date object
    end_date = 0    # A datetime.date object
    chart_exchange = 'tBTCUSD'

    candles = {}

    # Constants
    sort = -1
    limit = 1000
    chart_type = 'hist'

    # The class "constructor" - It's actually an initializer 
    def __init__(self, start_date, end_date, timeframe, chart_exchange):
        self.start_date = start_date
        self.end_date = end_date
        self.candles_timeframe = timeframe
        self.chart_exchange = chart_exchange

        self.candles = self._build_candles()

    @property
    def start_seconds_timestamp(self):
        return calendar.timegm(self.start_date.timetuple())

    @property
    def end_seconds_timestamp(self):
        return calendar.timegm(self.end_date.timetuple())

    def get_candle(timeframe):
        return candles

    def _get_url(timeframe, exchange, type):
        return 'https://api.bitfinex.com/v2/candles/trade:' + timeframe + ':' + exchange + '/' + type

    def _build_candles(self):
        candles = {}
        start_seconds_timestamp = self.start_seconds_timestamp
        end_seconds_timestamp = self.end_seconds_timestamp
        
        while(start_seconds_timestamp < end_seconds_timestamp):
            params = {
                'limit': self.limit,
                'start': start_seconds_timestamp,
                'end': end_seconds_timestamp,
                'sort': self.sort
            }
            url = _get_url(self.candles_timeframe, self.chart_exchange, self.chart_type)

            # Response with Section = "hist"
            # [
            #   [ MTS, OPEN, CLOSE, HIGH, LOW, VOLUME ], 
            #   ...
            # ]
            r = requests.get(url, params=params)
            # print('Total of candles: ' + str(len(r.json())))

            last_timestamp = 0
            for candle in r.json():
                last_timestamp = candle[0]
                candles[last_timestamp] = Candle(candle[0], candle[1], candle[2], candle[3], candle[4], candle[5])

            start_seconds_timestamp = start_seconds_timestamp + last_timestamp

        return candles