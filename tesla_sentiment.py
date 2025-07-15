import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

reddit = praw.Reddit(
    client_id='_2kTKSAXXUWlgGz2zzPl0w',
    client_secret='avb2BiKfRnx4pJPstSMYD_nxOtH5xA',
    user_agent='TeslaSentimentAnalysis by u/Alarming-Young1026'
)

subreddits = ['TeslaMotors']
queries = [
    "feature", "improve", "missing", "I want", "better",
    "problem", "frustrating", "complaint", "would buy if", "hate"
]

limit = 1000
posts = []
comments = []

analyzer = SentimentIntensityAnalyzer()

for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    for query in queries:
        print(f"Scraping: r/{subreddit_name} | Query: '{query}'")
        for submission in subreddit.search(query, limit=limit):

            if submission.selftext and submission.selftext.lower() not in ['[removed]', '[deleted]']:

                if submission.author:
                    try:
                        author_karma = submission.author.link_karma + submission.author.comment_karma

                        author_name = submission.author.name
                    except:
                        author_karma = None
                        author_name = '[unknown]'
                else:
                    author_karma = None
                    author_name = '[deleted]'
                post_sentiment = analyzer.polarity_scores(submission.selftext)['compound']

                posts.append({
                    'subreddit': subreddit_name,
                    'query': query,
                    'post_id': submission.id,
                    'title': submission.title,
                    'text': submission.selftext,
                    'url': submission.url,
                    'author': author_name,
                    'author_karma': author_karma,
                    'sentiment': post_sentiment
                })


                submission.comments.replace_more(limit=0)
                for comment in submission.comments[:10]:
                    if comment.body and comment.body.lower() not in ['[removed]', '[deleted]']:

                        if comment.author:
                            try:
                                c_author_karma = comment.author.link_karma + comment.author.comment_karma

                                c_author_name = comment.author.name
                            except:
                                c_author_karma = None
                                c_author_name = '[unknown]'
                        else:
                            c_author_karma = None
                            c_author_name = '[deleted]'
                        comment_sentiment = analyzer.polarity_scores(comment.body)['compound']

                        comments.append({
                            'subreddit': subreddit_name,
                            'query': query,
                            'post_id': submission.id,
                            'comment_id': comment.id,
                            'parent_id': comment.parent_id,
                            'body': comment.body,
                            'author': c_author_name,
                            'author_karma': c_author_karma,
                            'sentiment': comment_sentiment
                        })

            time.sleep(1)


df_posts = pd.DataFrame(posts)
df_comments = pd.DataFrame(comments)

df_posts.to_csv("tesla_reddit_sentiment_body_only_posts.csv", index=False)
df_comments.to_csv("tesla_reddit_sentiment_body_only_comments.csv", index=False)

print(f"✅ Data saved! {len(df_posts)} posts and {len(df_comments)} comments.")
