import os
import sys

from twsd.Preprocess import process_data

sys.path.append('../')
sys.path.append('./')




def main():
    cleaned_data = process_data("output/disasters-on-social-media-QueryResult.csv")
    print('\n'.join(cleaned_data))
    f = open("output/0", "a")
    f.write("\n".join(cleaned_data))
    f.close()

    # with open("output/cleaned_tweets_non_lemma.txt", "r+") as f:
    #     d = f.readlines()
    #     f.seek(0)
    #     for i in d:
    #         wordCount = len(i)
    #         if wordCount < 2:
    #             f.write(i)
    #     f.truncate()
    #     f.close()


if __name__ == '__main__':
    main()
