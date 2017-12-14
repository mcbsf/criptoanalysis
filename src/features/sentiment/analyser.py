from models.coin_chart import CoinChart, Candle
from models.subreddits import Subreddit, Comment


from features.sentiment.wnaffect.interface import WNAffect

class SentimentAnalyser(object):

    coin_chart = None
    subreddit = None
    time_emotion = {}


    def __init__(self, coin_chart, subreddit):
        
        self.coin_chart = coin_chart
        self.subreddit = subreddit
        self.time_emotion = self._build_time_emotion()


        wna = WNAffect('resources/wordnet-1.6/', 'resources/wn-domains-3.2/')
        emo = wna.get_emotion('angry', 'JJ')
        print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # print(emo)
        emo = wna.get_emotion('mad', 'JJ')
        print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # print(emo)
        emo = wna.get_emotion('annoyed', 'JJ')
        print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        # print(emo)
        emo = wna.get_emotion('hapy', 'JJ')
        # print(' -> '.join([emo.get_level(i).name for i in range(emo.level + 1)]))
        print(emo)


    def _build_time_emotion(self):
        
        time_emotion = {
            '12345678': (
                Candle,
                {
                    'emotion': freq
                }
            )

        }
        time_emotion = {}
        self.subreddit.get_tagged_term_time
        for term in self.subreddit.term_time:
            for postag in term
                emotion = wna.get_emotion(term, postag)
                for (_, ctimeframe) in postag
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