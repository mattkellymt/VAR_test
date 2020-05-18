import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from multiprocessing import Pool 
from functools import partial

def find_tweet_sentiment(tweet_id, tweet, vader):
    text = tweet["tweet_text"]
    sentiment = vader.polarity_scores(text)
    polarity = sentiment["compound"]
    return tweet_id, polarity

vader = SentimentIntensityAnalyzer()
find_vader_sentiment = partial(find_tweet_sentiment, vader=vader)
