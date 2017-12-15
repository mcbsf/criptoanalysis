import praw
import sys
from datetime import datetime, date
import calendar

def printu (str):
	print (str.encode ('utf-8'))

class Comment(object):
    
    words = []
    seconds_timestamp = 0
    score = 0
    _timeframe = 0 # Key for the time frame group of this specific comment

    def __init__(self, words, seconds_timestamp, score, group_seed):
        self.words = words
        self.seconds_timestamp = seconds_timestamp
        self.score = score

        self._timeframe = self._generate_timeframe_key(group_seed)

    @property
    def timeframe(self):
        return self._timeframe

    def _generate_timeframe_key(self, seed):
        return int(self.seconds_timestamp - (self.seconds_timestamp % seed))

class Subreddit(object):

    reddit = None
    subreddit = None
    comment_cleaner = None
    comments = []
    term_time = {}
    time_interval = 43200 # 43200 is Equivalent to 12 hours in seconds


    def __init__(self, client_id, client_secret, user_agent, start_date, end_date, title='Bitcoin', comment_cleaner=None, interval=43200):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self.subreddit = self.reddit.subreddit(title)
        self.start_date = start_date
        self.end_date = end_date
        self.comment_cleaner = comment_cleaner if comment_cleaner is not None else lambda word: word
        self.time_interval = interval
        self.comments = self._get_comments()
        self.term_time = self._build_term_time()

        # print('self.start_seconds_timestamp: ')
        # print(self.start_seconds_timestamp)
        # print('self.end_seconds_timestamp: ')
        # print(self.end_seconds_timestamp)
        # print('self.term_time: ')
        # print(self.term_time)

        # print ('comments: ')
        # print (self.comments)
        # print ('words: ')
        # print (self.comments[0].words)
        # print ('seconds_timestamp: ')
        # print (self.comments[0].seconds_timestamp)
        # print ('score: ')
        # print (self.comments[0].score)
        # print ('timeframe: ')
        # print (self.comments[0].timeframe)

    @property
    def start_ajusted_seconds_timestamp(self):
        return calendar.timegm(self.start_date.timetuple() + self.time_interval)

    @property
    def end_adjusted_seconds_timestamp(self):
        return calendar.timegm(self.end_date.timetuple() + self.time_interval)
    
    @property
    def start_seconds_timestamp(self):
        return calendar.timegm(self.start_date.timetuple())

    @property
    def end_seconds_timestamp(self):
        return calendar.timegm(self.end_date.timetuple())

    def get_term_tags(self, term):
        return self.term_time[term][1]
        
    def get_term_time(self, term, postag):
        return self.term_time[term][1][postag][1]

    def get_term_time_freq(self, term, postag, ctimeframe):
        return self.term_time[term][1][postag][1][str(ctimeframe)]

    def _build_term_time(self):
        # term_time = {
        #     'despite': (
        #         5,
        #         {
        #           'JJ': (
        #               3,
        #               {
        #                   '12345678': 2,
        #                   '8764321': 1
        #               }
        #            ),
        #            'NN': (
        #                2,
        #                {
        #                    '8764321': 2
        #                }
        #            )
        #         }
        #     )
        # }

        term_time = {}
        for comment in self.comments:
            ctimeframe = comment.timeframe + self.time_interval
            if ctimeframe < self.end_seconds_timestamp + self.time_interval:
                for (term, postag) in comment.words:
                    if term not in term_time:
                        term_time[term] = (0, {})
                    if postag not in term_time[term][1]:
                        term_time[term][1][postag] = (0, {})
                    if str(ctimeframe) not in term_time[term][1][postag][1]:
                        term_time[term][1][postag][1][str(ctimeframe)] = 0
                    
                    term_time[term][1][postag][1][str(ctimeframe)] += 1
                    term_time[term][1][postag] = (
                        term_time[term][1][postag][0] + 1,
                        term_time[term][1][postag][1]
                    )
                    term_time[term] = (
                        term_time[term][0] + 1, 
                        term_time[term][1]
                    )

        return term_time

    def _get_comments(self):
        all_comments = []
        start_seconds_timestamp = self.start_seconds_timestamp
        end_seconds_timestamp = 0

        sub_counter = 0
        while(start_seconds_timestamp < self.end_seconds_timestamp):
            end_seconds_timestamp = start_seconds_timestamp + self.time_interval
            print ('\nStart seconds_timestamp is: ', start_seconds_timestamp)
            for submission in self.subreddit.submissions(start_seconds_timestamp, end_seconds_timestamp):
                sub_counter += 1

                # print(submission.title)  # Output: the submission's title
                # print(submission.score)  # Output: the submission's score
                # print(submission.id)     # Output: the submission's ID
                # print(submission.url)    # Output: the URL the submission points to
                
                # comments_submission = submission.comments.list()
                # for comment in comments_submission:
                #   print(comment.words)

                submission.comments.replace_more(limit=None)
                comment_queue = submission.comments[:]  # Seed with top-level
                subsub_counter = 0
                while comment_queue:
                    subsub_counter += 1
                    comment = comment_queue.pop(0)
                    all_comments.append(
                        Comment(
                            words=self.comment_cleaner(comment.body), 
                            seconds_timestamp=comment.created, 
                            score=comment.score, 
                            group_seed=self.time_interval
                        )
                    )
                    # comment_queue.extend(comment.replies)
                    # break

                print ('\tA submission has ', subsub_counter, ' comments.')
                # if subsub_counter > 5:
                #     break
                #print(submission)
                # print('\n')

            # for comment in all_comments:
            #     printu(comment.words)
            #     print('\n')

            print ('\n\tFinished a total of ', sub_counter, ' submissions.\n')
            start_seconds_timestamp = end_seconds_timestamp
            # break

        return all_comments