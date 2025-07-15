import pandas as pd
import numpy as np

df = pd.read_csv("tesla_reddit_sentiment_body_only_posts.csv")

df = df.drop_duplicates(subset=['post_id'])

df['is_megathread'] = df['title'].str.contains("megathread", case=False, na=False)
df['is_bot'] = df['author'].str.lower().isin(["automoderator", "[unknown]"])

df['author_karma'] = df['author_karma'].fillna(-1)

karma_cap = df['author_karma'].quantile(0.99)
df['author_karma_capped'] = np.where(df['author_karma'] > karma_cap, karma_cap, df['author_karma'])

df['title'] = df['title'].str.strip()
df['text'] = df['text'].str.strip()

df['title_length'] = df['title'].str.len()
df['text_length'] = df['text'].str.len()

df.to_csv("tesla_posts_flagged_cleaned.csv", index=False)
