import os
import re
import praw

from datetime import datetime, date

from preprocessment.cleaner_builder import cleaner_builder

from models.coin_chart import CoinChart
from models.subreddits import Subreddit

from features.sentiment.analyser import SentimentAnalyser

start_date = datetime(2016, 11, 8, 7)
end_date = datetime(2016, 11, 8, 23)

print ('Building coin chart\n')

coin_chart = CoinChart(start_date=start_date, 
	end_date=end_date, 
	timeframe='12h', 
	chart_exchange='tBTCUSD')

print ('Start time: ', coin_chart.start_seconds_timestamp)
print ('End time: ', coin_chart.end_seconds_timestamp, '\n')
print ('Starting subreddit comments retrieval\n')

comment_cleaner = lambda document: cleaner_builder(
	document, 
	lower_words = False,
	fold_numbers = False,
	remove_stopwords = False, 
	do_stemming = False, 
	do_lemmatizing = False)

subreddits = Subreddit(client_id='g7g1TXRPCG1t4g', 
	client_secret='wMUyCgmjorwGoY9aOCE5jJm6Q3w', 
	user_agent='testscript by /u/mariocbsf', 
	start_date=start_date, 
	end_date=end_date, 
	title='Bitcoin', 
	comment_cleaner=comment_cleaner,
	interval=43200
) # 43200 is Equivalent to 12 hours in seconds 

print ('It\'s finished')

sa = SentimentAnalyser()