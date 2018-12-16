import datetime
import re
import nltk

import pandas as pd
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def nltk2wn_parts_of_speech_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatize(sentence):
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    wn_tagged = map(lambda x: (x[0], nltk2wn_parts_of_speech_tag(x[1])), nltk_tagged)
    res_words = []
    for word, tag in wn_tagged:
        if tag is None:
            res_words.append(word)
        else:
            res_words.append(lemmatizer.lemmatize(word, tag))
    return " ".join(res_words)


def process_data(raw_text):

    # Remove urls
    url_removed_text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", raw_text)

    # Remove user tagging
    tagging_removed_text = " ".join(filter(lambda x: x[0] != '@', url_removed_text.split()))

    # Remove hash_tags
    hash_tag_removed_text = " ".join(filter(lambda x: x[0] != '#', tagging_removed_text.split()))

    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", hash_tag_removed_text)

    # apply lemmatizer
    lemmatized_text = lemmatize(letters_only_text)

    # convert to lower case and split
    words = lemmatized_text.lower().split()

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
