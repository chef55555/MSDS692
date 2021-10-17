from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
csv_file = open('reencoded-tweets.csv', 'r', encoding='utf-8')
csv_reader = csv.reader(csv_file, delimiter=';' )
csv_out = open('scored-tweets.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_out, delimiter=';' )
csv_writer.writerow(["tweet_id", "timestamp", "sentiment_score"])
csv_file.flush()

# skip header
next(csv_reader)

sid_obj = SentimentIntensityAnalyzer()
for tweet in csv_reader:
    try:
        tweet_raw_text = tweet[3]
    except IndexError:
        print('\nError with line of file')
        print(tweet)
        continue
    # VADER provides a dictionary with positive, neutral and negative scores as well as a compound score
    sentiment_dict = sid_obj.polarity_scores(tweet_raw_text)
    # only using the compound score for now
    csv_writer.writerow([tweet[0],tweet[1],sentiment_dict['compound']])
