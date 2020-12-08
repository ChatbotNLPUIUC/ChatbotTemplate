import praw
import config
import pandas as pd
from pprint import pprint

reddit = praw.Reddit(client_id=config.CLIENT_ID,
                    client_secret=config.CLIENT_SECRET,
                    username=config.USERNAME,
                    password=config.PASSWORD,
                    user_agent='Reddit Scraper v1.0')

subreddit = reddit.subreddit('UIUC')

flair_template = subreddit.flair.link_templates 
flairs = [[flair['text'], flair['id']] for flair in flair_template]
flairs_of_interest = ['Freshman Question', 'Chambana Questions', 'AMA']

data = []

for flair in flairs:
    if flair[0] in flairs_of_interest:
        for submission in subreddit.search('flair:"' + flair[0] + '" self=1', sort='top', syntax='lucene', limit=None):
            if submission.num_comments > 0:
                submission.comment_sort = 'top'
                comments = submission.comments.list()
                # just top comment for now
                data.append([submission.title, comments[0].body])

print("Saved data")
df = pd.DataFrame(data, columns =['Question', 'Answer'])
df.to_csv('reddit_posts.csv', index=False, encoding='utf-8')