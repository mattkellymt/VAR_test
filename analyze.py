import os

from parallel import Parallel
from find_text_blob_sentiment import find_text_blob_sentiment
from find_vader_sentiment import find_vader_sentiment
from find_flair_sentiment import find_flair_sentiment
from load_tweets import load_tweets
from my_io import load_pickle, save_pickle
import warnings

if __name__ == "__main__":
    warnings.simplefilter("ignore")

    tweets = None
    sentiment_dir = "../sentiment/"
    sentiment_models = {
        "text_blob": find_text_blob_sentiment,
        "vader": find_vader_sentiment,
    }

    for model_name, model_function in sentiment_models.items():
        sentiment_path = os.path.join(sentiment_dir, model_name) + ".pickle"
        if not os.path.exists(sentiment_path):
            if tweets is None:
                tweets = load_tweets()
                tweets = list(tweets.items())

            results = Parallel(find_text_blob_sentiment, tweets, model_name)

            sentiment = {tweet_id: value for tweet_id, value in results}
            save_pickle(sentiment, sentiment_path)

    model_name = "flair"
    sentiment_path = os.path.join(sentiment_dir, model_name) + ".pickle"
    if not os.path.exists(sentiment_path):
        if tweets is None:
            tweets = load_tweets()
            tweets = list(tweets.items())
        sentiment = find_flair_sentiment(tweets, chunk_len=100000)
        sentiment_models[model_name] = sentiment
        save_pickle(sentiment, sentiment_path)
