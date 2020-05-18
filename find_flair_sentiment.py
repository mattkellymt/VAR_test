import flair
from multiprocessing import Pool, cpu_count
from functools import partial 
from progress import progress 
import time

def find_flair_sentiment(tweets, chunk_len=10000):
    model = flair.models.TextClassifier.load("en-sentiment")
    id_list, tweet_list = zip(*tweets)

    message = "Make Flair Sentences"
    lap_time = start_time = time.time()
    sentence_list = []

    for i, tweet in enumerate(tweet_list):
        lap_time = progress(i, lap_time, len(tweet_list), start_time, message)

        text = tweet["tweet_text"]
        sentence = flair.data.Sentence(text)
        sentence_list.append(sentence)
    progress(i, lap_time, len(tweet_list), start_time, message, done=True)

    chunks = []
    for i in range(0, len(sentence_list), chunk_len):
        chunk = sentence_list[i: i + chunk_len]
        chunks.append(chunk)

    message = "Predict Flair Sentiment"
    lap_start = start_time = time.time()
    polarity_list = []

    for i, chunk in enumerate(chunks):
        try:
            model.predict(chunk)
        except:
            print(chunk)
            for x in chunk:
                model.predict(x)

        lap_start = progress(i, lap_start, len(chunks), start_time, message)
        for sentence in chunk:
            try:
                sentiment = sentence.labels[0]
            except:
                label = None
                polarity = 0
            else:
                label = sentiment.value.lower()
                polarity = sentiment.score

            if label == "negative":
                polarity = -polarity
            polarity_list.append(polarity)
    progress(i, lap_start, len(chunks), start_time, message, done=True)

    sentiment = {
        tweet_id: polarity 
        for tweet_id, polarity in zip(id_list, polarity_list)
    }
    return sentiment
    