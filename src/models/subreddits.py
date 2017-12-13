import praw
import sys
from datetime import datetime, date
import calendar

def printu (str):
	print (str.encode ('utf-8'))

class Comment(object):
    
    body = ''
    time_stamp = 0 #converter de sec
    score = 0


    def __init__(self, body, time_stamp, score):
    
        self.body = body
        self.time_stamp = time_stamp
        self.score = score


class Subreddit(object):

    reddit = None
    subreddit = None
    comments_by_time = {} #testar se faz função chão da divisão do tempo por 12h em milisec

    def __init__(self, client_id, client_secret, user_agent, title, start_date, end_date, interval):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self.subreddit = self.reddit.subreddit(title)
        self.start_date = start_date
        self.end_date = end_date

        # print(self.start_seconds_timestamp)
        # print(self.end_seconds_timestamp)

        self.comments_by_time = self._organize_comments(self._get_comments(interval), interval)

    def _get_comments(self, interval):
        all_comments = []
        start_seconds_timestamp = self.start_seconds_timestamp
        end_seconds_timestamp = self.end_seconds_timestamp

        sub_counter = 0
        while(start_seconds_timestamp < end_seconds_timestamp):
            for submission in self.subreddit.submissions(start_seconds_timestamp, start_seconds_timestamp + interval):
                sub_counter += 1

                # print(submission.title)  # Output: the submission's title
                #print(submission.score)  # Output: the submission's score
                #print(submission.id)     # Output: the submission's ID
                #print(submission.url)    # Output: the URL the submission points to
                
                # comments_submission = submission.comments.list()
                # #for comment in comments_submission:
                # #   print(comment.body)

                submission.comments.replace_more(limit=None)
                comment_queue = submission.comments[:]  # Seed with top-level
                subsub_counter = 0
                while comment_queue:
                    subsub_counter += 1
                    comment = comment_queue.pop(0)
                    all_comments.append(Comment(comment.body, comment.created, comment.score))
                    comment_queue.extend(comment.replies)

                print ('\tA submission have ', subsub_counter, ' comments.')
                #print(submission)
                # print('\n')

            # for comment in all_comments:
            #     printu(comment.body)
            #     print('\n')

            print ('\n\t\tFinished a total of ', sub_counter, ' submissions.\n')
            start_seconds_timestamp = start_seconds_timestamp + interval

        return all_comments

    def _organize_comments(self, comments, interval):

        for comment in comments:
            if (comment.time_stamp < self.end_seconds_timestamp):
                self.comments_by_time[comment.time_stamp-(comment.time_stamp%interval)] = comment #separa os comentários por grupos de 12 em 12h. 4320 = 12h em segundos

    @property
    def start_seconds_timestamp(self):
        return calendar.timegm(self.start_date.timetuple())

    @property
    def end_seconds_timestamp(self):
        return calendar.timegm(self.end_date.timetuple())