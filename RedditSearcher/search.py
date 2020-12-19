import praw
import pandas as pd

def setup_subreddit(sub_name='UIUC'):
    reddit = praw.Reddit(client_id='pErOBxjzD-ahwA',
                        client_secret='qB5wvHLmg6do0ITuBhWkQ61xpEl25g',
                        username='uiuc-chatbot',
                        password='what_is_bert',
                        user_agent='Reddit Searcher v1.0')

    subreddit = reddit.subreddit(sub_name)
    return subreddit

def search_subreddit(subreddit, query, sort='relevance', num_posts=None, num_comments=1):
    data = []

    for submission in subreddit.search(query + ' self:yes', sort, syntax='lucene', limit=num_posts):
        if submission.num_comments > 0:
            submission.comment_sort = 'top'
            comments = submission.comments.list()
            top_comments = []

            for x in range(min(num_comments, len(comments))):
                top_comments.append(comments[x].body)

            data.append([submission.title + ' ' + submission.selftext, top_comments])

    df = pd.DataFrame(data, columns =['Question', 'Answer'])
    return df

# Sample
sub = setup_subreddit()
data = search_subreddit(sub, 'CR/NC', num_posts=5)