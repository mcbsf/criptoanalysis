from models.coin_chart import CoinChart, Candle
from models.subreddits import Subreddit, Comment

from features.sentiment.wnaffect.interface import WNAffect

import plotly as py
import plotly.graph_objs as go

def printu (str):
	print (str.encode ('utf-8'))

class SentimentAnalyser(object):

    coin_chart = None
    subreddit = None
    time_emotion = {}
    wna = None

    def __init__(self, coin_chart, subreddit):
        self.coin_chart = coin_chart
        self.subreddit = subreddit
        self.wna = WNAffect('resources/wordnet-1.6/', 'resources/wn-domains-3.2/')
        print('Starting time emtion building')
        self.time_emotion = self._build_time_emotion()

        # emo = wna.get_emotion('angry', 'JJ')
        # print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # # print(emo)
        # emo = wna.get_emotion('mad', 'JJ')
        # print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # # print(emo)
        # emo = wna.get_emotion('annoyed', 'JJ')
        # print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # # print(emo)
        # emo = wna.get_emotion('hapy', 'JJ')
        # # print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # print(emo)

    def perform_analysis(self):
        chart_data = []
        histogram_data = []
        histogram = {}
        c = 0
        for ctimeframe in self.time_emotion:
            (candle, emotion_dic) = self.time_emotion[ctimeframe]
            chart_data.append(
                go.Box(
                    name=candle.datetime,
                    y=[candle.open_price, candle.close_price, candle.higher_price, candle.lower_price],
                    boxpoints='all',
                    jitter=0.3
                )
            )

            temp = {}
            for index, emotion in enumerate(emotion_dic):
                if str(index) not in temp:
                    temp[str(index)] = 0
                
                temp[str(index)] += 1
            
            for index, emotion in enumerate(emotion_dic):  
                if str(index) not in histogram:  
                    histogram[str(index)] = []

                histogram[str(index)].append(emotion_dic[emotion])

            c = candle.datetime
            
        print (histogram)
        h = []
        for index in histogram:
            histogram_data.append(
                go.Histogram(
                    name=str(index),
                    x=c,
                    opacity=0.5
                )
            )

        print(histogram_data)

        data = [chart_data, histogram_data]
        py.offline.plot(data, filename='box-histogram')
        # "layout": go.Layout(title="Sentiment analysis over bitcoin price chart")

    def _build_time_emotion(self):
        # time_emotion = {
        #     '12345678': (
        #         Candle,
        #         {
        #             'emotion': freq
        #         }
        #     )

        # }
        time_emotion = {}
        for term in self.subreddit.term_time:
            # printu(term)
            for postag in self.subreddit.get_term_tags(term):
                # printu(postag)
                emotion = self.wna.get_emotion(term, postag)
                if emotion is not None:
                    for ctimeframe in self.subreddit.get_term_time(term, postag):
                        if str(ctimeframe) in self.coin_chart.candles:
                            if str(ctimeframe) not in time_emotion:
                                time_emotion[str(ctimeframe)] = (None, {})
                            if emotion not in time_emotion[str(ctimeframe)][1]:
                                time_emotion[str(ctimeframe)][1][emotion] = 0

                            time_emotion[str(ctimeframe)][1][emotion] += self.subreddit.get_term_time_freq(term, postag, ctimeframe)

                            time_emotion[str(ctimeframe)] = (
                                self.coin_chart.get_candle(int(ctimeframe) + self.subreddit.time_interval),
                                time_emotion[str(ctimeframe)][1]
                            )
                    
        return time_emotion