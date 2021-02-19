import re
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
from TwitterStream import Listener
from tweepy import Stream


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = ######
        consumer_secret = #####
        access_token = #####
        access_token_secret = #####

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth, wait_on_rate_limit= True, wait_on_rate_limit_notify=True)
        except:
            print("Error: Authentication Failed")

    def create_wordcloud(self, text, stopwords, title):
        mask = np.array(Image.open("cloud.png"))
        wc = WordCloud(background_color="white",
                      mask = mask,
                      max_words=300,
                      stopwords=stopwords)
        wc.generate((self.clean_tweet(str(text))))
        wc.to_file("{}.png".format(title))


    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ /\S+)", " ", tweet).split())

    def twitter_stream(self, keyword_list):
        output = open('_'.join(keyword_list) + '.txt', 'w', encoding="utf-8")
        listener = Listener(output_file=output)
        stream = Stream(auth=self.auth, listener=listener)
        try:
            print('Start streaming.')
            stream.filter(track=keyword_list, languages=['en'])
        except KeyboardInterrupt:
            print("Stopped.")
        finally:
            print('Done.')
            stream.disconnect()
            output.close()

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = tweepy.Cursor(self.api.search, q=query, include_rts=False).items(count)
            # fetched_tweets = tweepy.Cursor(self.api.user_timeline, screen_name=query, include_rts=True).items(count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['url'] = 'https://twitter.com/'+tweet.user.screen_name + '/status/' + tweet.id_str
                parsed_tweet['time'] = tweet.created_at
                parsed_tweet['user_name'] = tweet.user.name
                parsed_tweet['retweet_count'] = tweet.retweet_count
                parsed_tweet['favorite_count'] = tweet.favorite_count
                tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():

    # Step 0. Initialize Parameters
    tweetAnalyzer = TwitterClient()
    key_word = "Oregon State University"
    count = 1000

    # Step 1.  Collect Tweets
    # tweets = tweetAnalyzer.get_tweets(key_word, count)
    # tweets_df = pd.DataFrame(tweets)
    # tweets_df.to_csv("collected tweets ({}).csv".format(key_word), index=None)

    # Step 2. Word Cloud
    # tweets_df = pd.read_csv("collected tweets ({}).csv".format(key_word))
    # stopwords = set(STOPWORDS)
    # tweetAnalyzer.create_wordcloud(tweets_df['text'].values, stopwords, key_word)


    # Step 3. Sentiment Analysis
    # tweets_df = pd.read_csv("collected tweets ({}).csv".format(key_word))
    # tweets_df['sentiment'] = tweets_df['text'].apply(tweetAnalyzer.get_tweet_sentiment)
    # tweets_df.to_csv("collected tweets ({}).csv".format(key_word), index=None)


    # Step 4. Word Cloud of Positive and Negative
    # tweets_df = pd.read_csv("collected tweets ({}).csv".format(key_word))
    # pos_tweets_df = tweets_df.loc[tweets_df['sentiment']=='positive']
    # neg_tweets_df = tweets_df.loc[tweets_df['sentiment']=='negative']
    # stopwords = set(STOPWORDS)
    # tweetAnalyzer.create_wordcloud(pos_tweets_df['text'].values, stopwords, key_word+' pos')
    # tweetAnalyzer.create_wordcloud(neg_tweets_df['text'].values, stopwords, key_word+' neg')

    # Step 5. Stream
    key_word = ['oregon state university']
    tweetAnalyzer.twitter_stream(key_word)



if __name__ == "__main__":
    # calling main function
    main()
