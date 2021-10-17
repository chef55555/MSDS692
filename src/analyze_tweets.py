import pandas as pd

# Read in the tweets and scores
tweet_scores = pd.read_csv('scored-tweets.csv', sep=';')
tweets = pd.read_csv('reencoded-tweets.csv', sep=';')

# convert timestamp strings to timestamp classes
tweet_scores.timestamp = pd.to_datetime(tweet_scores.timestamp)
tweets.timestamp = pd.to_datetime(tweets.timestamp)

# raw count by date and average score
tweet_counts_by_day = tweet_scores.groupby([tweet_scores.timestamp.dt.date]).count()
sentiment_by_day = tweet_scores.groupby([tweets.timestamp.dt.date]).mean()

print('Tweet counts by day\n')
print(tweet_counts_by_day[ "sentiment_score"])

print('Average sentiment score by day\n')
print(sentiment_by_day[ "sentiment_score"])

# Join the tweets to the scores and sort by score
joined_tweets =pd.merge(tweets, tweet_scores, on="tweet_id")
sorted_tweets = joined_tweets.sort_values(by=['sentiment_score'])
pd.set_option('display.max_colwidth', None)

# print first 10 and last 10 will give the highest and lowest scored tweets
print('\nTop positive tweets\n')
print (sorted_tweets[['text', 'sentiment_score']].iloc[0:10])
print('\nTop negative tweets\n')
print (sorted_tweets[['text', 'sentiment_score']].iloc[-11:-1])
