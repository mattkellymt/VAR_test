from my_io import load_pickle, save_pickle

def load_tweets(path="../tweets/mined.pickle"):
    print("Loading Tweets")

    tweets = load_pickle(path)
    return tweets 
