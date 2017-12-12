import praw
import sys

def printu (str):
	print (str.encode ('utf-8'))

reddit = praw.Reddit(client_id='g7g1TXRPCG1t4g',
                     client_secret='wMUyCgmjorwGoY9aOCE5jJm6Q3w',
                     user_agent='testscript by /u/mariocbsf')

subreddit = reddit.subreddit('Bitcoin')

# print(subreddit.display_name)
# print(subreddit.title)
# printu (subreddit.description)

for submission in subreddit.hot(limit=10):
    #print(submission.title)  # Output: the submission's title
    #print(submission.score)  # Output: the submission's score
    #print(submission.id)     # Output: the submission's ID
    #print(submission.url)    # Output: the URL the submission points to
    
    all_comments = submission.comments.list()
    
    #for comment in all_comments:
    #   print(comment.body)

    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]  # Seed with top-level
    while comment_queue:
        comment = comment_queue.pop(0)
        printu(comment.body)
        comment_queue.extend(comment.replies)
    #print(submission)
    break
    print('\n')