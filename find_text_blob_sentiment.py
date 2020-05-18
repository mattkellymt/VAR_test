from textblob import TextBlob
from multiprocessing import Pool 
import time 

def find_text_blob_sentiment(args):
    tweet_id, tweet = args
    text = tweet["tweet_text"]
    blob = TextBlob(text)
    polarity = blob.polarity
    return tweet_id, polarity

