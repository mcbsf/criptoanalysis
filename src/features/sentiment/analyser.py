from models.coin_chart import CoinChart, Candle
from models.subreddits import Subreddit, Comment


from features.sentiment.wnaffect.interface import WNAffect

class SentimentAnalyser(object):

    coin_chart = None
    subreddit = None
    time_emotion = {}
    wna = None


    def __init__(self, coin_chart, subreddit):
        
        self.coin_chart = coin_chart
        self.subreddit = subreddit
        print('Starting time emtion building')
        self.time_emotion = self._build_time_emotion()


        self.wna = WNAffect('resources/wordnet-1.6/', 'resources/wn-domains-3.2/')
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
        for ctimeframe in self.time_emotion:
            (candle, emotion_dic) = self.time_emotion[ctimeframe]
            print(candle.percentage_variation)
            print(emotion_dic)

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
            for postag in term:
                emotion = self.wna.get_emotion(term, postag)
                for (_, ctimeframe) in postag:
                    if ctimeframe not in time_emotion:
                        time_emotion[ctimeframe] = (None, {})
                    if emotion not in time_emotion[ctimeframe][1]:
                        time_emotion[ctimeframe][1][emotion] = 0

                    time_emotion[ctimeframe][1][emotion] += self.subreddit.term_time[term][1][postag][1][ctimeframe]   

                    time_emotion[ctimeframe] = (
                        self.coin_chart.get_candle(ctimeframe+self.subreddit.time_interval),
                        time_emotion[ctimeframe][1]
                    )
                    


        return time_emotion