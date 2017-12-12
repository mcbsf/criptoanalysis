from datetime import datetime, date
import calendar

class CoinChart(object):
    candles_time_frame = '12h'
    start_date = 0 # A datetime.date object
    end_date = 0 # A datetime.date object

    candles = None

    # The class "constructor" - It's actually an initializer 
    def __init__(self, time_frame, start_date, end_date):
        self.candles_time_frame = time_frame
        self.start = start_date
        self.end = end_date

        self.candles = self._build_candles

    @property
    def start_timestamp(self):
        return calendar.timegm(start_date.timetuple())

    @property
    def end_timestamp(self):
        return calendar.timegm(end_date.timetuple())



def make_coin_chart(name, age, major):
    student = Student(name, age, major)
    return student