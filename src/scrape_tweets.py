import tweepy
import csv
import time


consumer_key = 'YOUR_KEY_HERE'
consumer_secret = 'YOUR_SECRET_HERE'
access_token = 'YOUR_TOKEN_HERE'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET_HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# handles the case of making too many requests within a timeperiod
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except StopIteration:
            break
        except tweepy.errors.TooManyRequests:
            print("Too many requests, sleeping for 15 minutes")
            time.sleep(15 * 60)

csv_file = open('scraped-tweets.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file, delimiter=';' )
# write header
csv_writer.writerow(["tweet_id", "timestamp", "entities", "text"])
csv_file.flush()
# Remove the "since" operator from this query before you use it for real, or at least change it
# it prevents returning too many results until you are ready
query = "AAPL lang:en -RT"
label = "30"
count =0
# Use maxResults=500 if you are using a paid developer, it will cut down on the number of requests you use
# swap the next two lines to remove limit for testing. The fromDate string format is YYYYMMDD0000
for tweet in limit_handled(tweepy.Cursor(api.search_30_day,label=label, query=query, fromDate='202110170000').items()):
#for tweet in limit_handled(tweepy.Cursor(api.search_30_day,label=label, query=query).items()):
    tweet_text = ""
    if tweet.truncated:
        tweet_text= tweet.extended_tweet['full_text']
    else:
        tweet_text=tweet.text
    # FIXME: need to find another way to remove newlines and other troublesome characters, tweet_text.encode("utf-8") is wrong
    csv_writer.writerow([tweet.id, tweet.created_at, tweet.entities["symbols"], tweet_text.encode("utf-8")])
    count+=1
    if count %100 ==0:
        print(count)
        
csv_file.flush()