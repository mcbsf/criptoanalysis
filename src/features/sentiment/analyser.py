from features.sentiment.wnaffect.interface import WNAffect

class SentimentAnalyser(object):

    def __init__(self):
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