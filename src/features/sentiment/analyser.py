from models.coin_chart import CoinChart, Candle
from models.subreddits import Subreddit, Comment

from features.sentiment.wnaffect.interface import WNAffect
from features.correlation import pearson

import plotly as py
import plotly.graph_objs as go

def printu (str):
	print (str.encode ('utf-8'))

class SentimentAnalyser(object):

    coin_chart = None
    subreddit = None
    time_emotion = {}
    wna = None
    correlation_matrix = None

    def __init__(self, coin_chart=None, subreddit=None):
        self.coin_chart = coin_chart
        self.subreddit = subreddit
        self.wna = WNAffect('resources/wordnet-1.6/', 'resources/wn-domains-3.2/')
        self.time_emotion = self._build_time_emotion()

        # emo = self.wna.get_emotion('angry', 'JJ')
        # print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # # print(emo)
        # emo = self.wna.get_emotion('mad', 'JJ')
        # print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # # print(emo)
        # emo = self.wna.get_emotion('annoyed', 'JJ')
        # print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # # print(emo)
        # emo = self.wna.get_emotion('hapy', 'JJ')
        # # print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # print(emo)

    def perform_analysis(self):
        timestamps = []
        high_prices = []
        low_prices = []
        open_prices = []
        close_prices = []
        percentage_variations = []
        emotion_data = {}
        all_emotions = []
        print(self.time_emotion)
        
        for ctimeframe in self.time_emotion:
            (candle, emotion_dic) = self.time_emotion[ctimeframe]
            # (candle, emotion_dic_prov) = self.time_emotion[ctimeframe]
            
            # emotion_dic = {}
            # for emotion in emotion_dic_prov:
            #     if str(emotion) != 'None':                
            #         if emotion.get_level(5) not in emotion_dic:
            #             emotion_dic[str(emotion.get_level(5))] = 0
                    
            #         emotion_dic[str(emotion.get_level(5))] += 1

            print ('AQUIIIIIIIIII')
            # print (emotion_dic_prov)
            print (emotion_dic)

            high_prices.append(candle.higher_price)
            low_prices.append(candle.lower_price)
            open_prices.append(candle.open_price)
            close_prices.append(candle.close_price)
            percentage_variations.append((candle.percentage_variation, candle.seconds_timestamp))

            timestamps.append((candle.seconds_timestamp, candle.datetime))
            for emotion in emotion_dic:
                if str(emotion) != 'None':
                    if candle.seconds_timestamp not in emotion_data:
                        emotion_data[candle.seconds_timestamp] = {}
                    if str(emotion) not in emotion_data[candle.seconds_timestamp]:
                        emotion_data[candle.seconds_timestamp][str(emotion)] = 0
                        
                    # last_pos = len(emotion_data[str(emotion)])-1
                    # emotion_data[str(emotion)][last_pos] += emotion_dic[str(emotion)]
                    emotion_data[candle.seconds_timestamp][str(emotion)] += emotion_dic[str(emotion)]

            for emotion in emotion_dic:
                if emotion not in all_emotions:
                    all_emotions.append(str(emotion))
            
            # for emotion in emotion_data:
            #     emotion_data[str(emotion)].append(0)

        print('opaaa')
        percentage_variations.sort(key=lambda tup: tup[1])
        timestamps.sort(key=lambda tup: tup[0])
        print(percentage_variations)

        high_data = go.Scatter(
            name='high price',
            x=[tup[1] for tup in timestamps],            
            y=high_prices,
            line =  dict(
                color = ('rgb(51, 204, 51)'),
                width = 4,
                dash = 'dot'
            )
        )
        low_data = go.Scatter(
            name='low price',
            x=[tup[1] for tup in timestamps],            
            y=low_prices,
            line =  dict(
                color = ('rgb(255, 80, 80)'),
                width = 4,
                dash = 'dot'
            )
        )
        open_data = go.Scatter(
            name='open price',
            x=[tup[1] for tup in timestamps],            
            y=open_prices,
            line =  dict(
                color = ('rgb(204, 51, 255)'),
                width = 4
            )
        )
        close_data = go.Scatter(
            name='close price',
            x=[tup[1] for tup in timestamps],            
            y=close_prices,
            line =  dict(
                color = ('rgb(204, 51, 255)'),
                width = 4
            )
        )
        percentage_data = go.Scatter(
            name='Percentage variation',
            x=[tup[1] for tup in timestamps],            
            y=[tup[0]*100 for tup in percentage_variations],
            line =  dict(
                color = ('rgb(0, 0, 102)'),
                width = 4
            )
        )

        # chart_data = [low_data, high_data, open_data, close_data]
        chart_data = [low_data, high_data, open_data, close_data, percentage_data]

        totallen = {}
        # first_time = True
        for (timestamp, _) in timestamps:
            print('emotion_data[timestamp].values')
            print(emotion_data[timestamp])
            totallen[timestamp] = sum(emotion_data[timestamp].values())
            #     if first_time:
            #         totallen.append(value)
            #     else:
            #         totallen[i] += value
            # first_time = False

            # totallen += len(emotion_data[str(emotion)])
        
        print (totallen)
        # print ([value/totallen for value in emotion_data[emotion]])
        # print (emotion_data)
        ordered_emotions = {}
        for (timestamp, _) in timestamps:
            for emotion in all_emotions:
                if emotion not in ordered_emotions:
                    ordered_emotions[emotion] = []
                if emotion in emotion_data[timestamp]:
                    ordered_emotions[emotion].append(emotion_data[timestamp][emotion]/totallen[timestamp])
                else:
                    ordered_emotions[emotion].append(0)
            
        for emotion in ordered_emotions:
            chart_data.append(
                go.Bar(
                    name=str(emotion),
                    x=[tup[1] for tup in timestamps],
                    y=[value*100 for value in ordered_emotions[emotion]]
                    # y=emotion_data[emotion]
                )
            )
        # chart_data.append()
            
        py.offline.plot({
            'data': chart_data,
            'layout': go.Layout(title="Sentiment analysis over bitcoin price chart", barmode='stack')
        })

    def build_correlation_matrix(self):
        #achar correlação
        #high_prices = []
        #low_prices = []
        #open_prices = []
        #close_prices = []
        #percentage_variations = []
        #emotion -> freq
        correlation_matrix = []
        counter = 0

        python_array = [1,2,3,4,5,6]
        np_array = np.array(python_array)
        

        for time in self.time_emotion:
	        #time[0] é o candle
            instance = []
	        for attr in time[0]:
	    	    #correlation_matrix[counter].append(attr)
                instance.append(attr)
	        #time[1] pega o dicionario de emoções->freq
	        for emotion, frequence in time[1]:
	    	    #correlation_matrix[counter].append(frequence)
                instance.append(frequence)
            np_instance = np.array(instance)
            correlation_matrix.append(np_instance)
	        #counter = counter + 1
        np_correlation_matrix = np.array(correlation_matrix)
        self.correlation_matrix = np_correlation_matrix
    
    def do_correlation(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix)-1):
                if(i!=(j+1)):
                    corelation_value = pearson.population_correlation(matrix, i, j+1)
                    #escrever correlação


    def _build_time_emotion(self):
        # time_emotion = {
        #     '12345678': (
        #         Candle,
        #         {
        #             'emotion': freq
        #         }
        #     )

        # }
        print ('\tBuilding paranaue')
        time_emotion = {}
        for term in self.subreddit.term_time:
            # printu(term)
            for postag in self.subreddit.get_term_tags(term):
                # printu(postag)
                emotion = self.wna.get_emotion(term, postag)
                if emotion is not None:
                    # print ('\t->', self.subreddit.get_term_time(term, postag))
                    for ctimeframe in self.subreddit.get_term_time(term, postag):
                        # print ('\t\t->', ctimeframe)
                        
                        if str(ctimeframe) in self.coin_chart.candles:

                            if str(ctimeframe) not in time_emotion:
                                print('eitcha')
                                time_emotion[str(ctimeframe)] = (None, {})
                            if str(emotion.get_level(5)) not in time_emotion[str(ctimeframe)][1]:
                                time_emotion[str(ctimeframe)][1][str(emotion.get_level(5))] = 0

                            time_emotion[str(ctimeframe)][1][str(emotion.get_level(5))] += self.subreddit.get_term_time_freq(term, postag, ctimeframe)

                            time_emotion[str(ctimeframe)] = (
                                self.coin_chart.get_candle(int(ctimeframe) + self.subreddit.time_interval),
                                time_emotion[str(ctimeframe)][1]
                            )

        print(time_emotion)
                    
        return time_emotion