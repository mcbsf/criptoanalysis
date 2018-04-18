import os
import re
import praw

from datetime import datetime, date

from preprocessment.cleaner_builder import cleaner_builder

from models.coin_chart import CoinChart
from models.subreddits import Subreddit

from features.sentiment.analyser import SentimentAnalyser

start_year = 2018
start_month = 3
start_day = 27
end_year = 2018
end_month = 4
end_day = 1

start_date = datetime(start_year, start_month, start_day, 12)
end_date = datetime(end_year, end_month, end_day, 12)

print ('Building coin chart\n')

coin_chart = CoinChart(start_date=start_date, 
	end_date=end_date, 
	timeframe='12h', 
	chart_exchange='tBTCUSD')

# print ('Coin chart start time: ', coin_chart.start_seconds_timestamp) # UTC Time date
# print ('Coin chart end time: ', coin_chart.end_seconds_timestamp, '\n')
print ('\nStarting subreddit comments retrieval\n')

start_date = datetime(start_year, start_month, start_day, 00)
end_date = datetime(end_year, end_month, end_day, 00)
comment_cleaner = lambda document: cleaner_builder(
	document,
	lower_words = True,
	fold_numbers = False,
	remove_stopwords = True, 
	do_stemming = True, 
	do_lemmatizing = False)

subreddit = Subreddit(client_id='g7g1TXRPCG1t4g', 
	client_secret='wMUyCgmjorwGoY9aOCE5jJm6Q3w', 
	user_agent='testscript by /u/mariocbsf', 
	start_date=start_date, 
	end_date=end_date, 
	title='Bitcoin', 
	comment_cleaner=comment_cleaner,
	interval=43200
) # 43200 is Equivalent to 12 hours in seconds 

# print ('subreddits start time: ', subreddit.start_seconds_timestamp)
# print ('subreddits end time: ', subreddit.end_seconds_timestamp, '\n')

print ('It\'s finished')

print('Starting time sentiment analyser builder')
sa = SentimentAnalyser(coin_chart, subreddit)


#itera sobre os tempos
sa.build_correlation_matrix()

print('Starting time sentiment analysis')
sa.perform_analysis()