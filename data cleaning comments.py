import pandas as pd
import numpy as np

df = pd.read_csv("tesla_reddit_sentiment_body_only_comments.csv")

df = df.drop_duplicates()

df['is_bot'] = df['author'].str.lower() == "automoderator"
df['is_deleted'] = df['author'].str.lower() == "[deleted]"

template_phrases = [
    "support thread", "use our stickied", "as we are not a support sub"
]
df['is_template'] = df['body'].str.lower().apply(
    lambda x: any(p in x for p in template_phrases)
)

df = df.drop_duplicates(subset=["comment_id"])

df['author_karma'] = df['author_karma'].fillna(-1)
karma_cap = df['author_karma'].quantile(0.99)
df['author_karma_capped'] = np.where(df['author_karma'] > karma_cap, karma_cap, df['author_karma'])

df['body_length'] = df['body'].str.len()
df['is_short'] = df['body_length'] < 10

df.to_csv("tesla_comments_flagged_cleaned.csv", index=False)
