import re
from nltk.corpus import stopwords
import pandas as pd
import datetime


def process_data(raw_text):

    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split
    words = letters_only_text.lower().split()

    # remove stopwords
    stopwords_list = set(stopwords.words("english"))
    meaningful_words = [w for w in words if w not in stopwords_list]

    # join the cleaned words in a list
    cleaned_word_list = " ".join(meaningful_words)

    return cleaned_word_list


def pre_process(data_set):
    tweets_df = pd.read_csv(data_set, delimiter='\t', header=None)

    num_tweets = tweets_df.shape[0]
    print("Total tweets: " + str(num_tweets))

    cleaned_tweets = []
    print("Beginning processing of tweets at: " + str(datetime.datetime.now()))

    for i in range(num_tweets):
        cleaned_tweet = process_data(tweets_df.iloc[i][1])
        cleaned_tweets.append(cleaned_tweet)
        if i % 10000 == 0:
            print(str(i) + " tweets processed")

    print("Finished processing of tweets at: " + str(datetime.datetime.now()))
    return cleaned_tweets
