import os
import re
import praw

from datetime import datetime, date

from models.coin_chart import CoinChart, Candle
from models.subreddits import Subreddit

start_date = datetime(2016, 11, 8, 8)
end_date = datetime(2016, 11, 9, 8)

print ('Building coin chart\n')

coin_chart = CoinChart(start_date=start_date, 
	end_date=end_date, 
	time_frame='12h', 
	chart_exchange='tBTCUSD')

print ('Starting subreddit comments retrieval\n')

subreddits = Subreddit(client_id='g7g1TXRPCG1t4g', 
	client_secret='wMUyCgmjorwGoY9aOCE5jJm6Q3w', 
	user_agent='testscript by /u/mariocbsf', 
	title='Bitcoin', 
	start_date=start_date, 
	end_date=end_date, 
	interval=8640) # 4320 is Equivalent to 12 hours in seconds

print ('It\'s finished')