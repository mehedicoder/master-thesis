import re
from nltk.corpus import stopwords
import nltk
import pandas as pd
import datetime
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

def get_wordnet_pos(word):

    #Map POS tag to first character lemmatize() accepts

    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def pre_process(raw_text):

    # remove urls
    url_pattern = 'http://\S+|https://\S+'
    url_removed_text = re.sub(url_pattern, '', str(raw_text))

    # remove RT and cc
    RT_CC_removed_text = re.sub('RT|cc', '', raw_text)

    # remove hashtags
    hashtag_removed_text = re.sub('#\S+', '', RT_CC_removed_text)

    # remove mentions
    tweet = re.sub('@\S+', '', hashtag_removed_text)

    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", str(tweet))

    # shortword removed
    shortword_removed_words = re.sub(r'\b\w{1,2}\b', '', letters_only_text)

    # convert to lower case and split
    words = shortword_removed_words.lower().split()

    only_existent_words = []
    wpt = WordPunctTokenizer()

    #for s in words:
        #tokens = wpt.tokenize(s)
        #if tokens:  # check if empty string
            #for t in tokens:
                #if wordnet.synsets(t):
                    #only_existent_words.append(t)  # remove all non-existent words


    # remove stopwords
    stopword_set = set(stopwords.words("english"))
    meaningful_words = [w for w in words if w not in stopword_set]

    # join the cleaned words in a list
    #cleaned_word_list = " ".join(meaningful_words)

    # lemmatize the words

    #nltk.download('averaged_perceptron_tagger')

    lemmatized_output = []
    wnl = WordNetLemmatizer()
    lemmatized_output = [wnl.lemmatize(w, get_wordnet_pos(w)) for w in meaningful_words]

    lemmatized_wordlist = " ".join(meaningful_words)

    return lemmatized_wordlist


def process_data(data_set):
    tweets_df = pd.read_csv(data_set, delimiter='\t', header=None)

    num_tweets = tweets_df.shape[0]
    print("Total tweets: " + str(num_tweets))

    cleaned_tweets = []
    print("Beginning processing of tweets at: " + str(datetime.datetime.now()))

    for i in range(num_tweets):
        cleaned_tweet = pre_process(tweets_df.iloc[i][1])
        cleaned_tweets.append(cleaned_tweet)
        if i % 10000 == 0:
            print(str(i) + " tweets processed")

    print("Finished processing of tweets at: " + str(datetime.datetime.now()))
    return cleaned_tweets
