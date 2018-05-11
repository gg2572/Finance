from TwitterSearch import *
import time

import sys
sys.path.append('/Users/ggao/Documents/Finance')

from GetOldTweets import got
import json
with open('/Users/ggao/.twitter_keys.json', 'r') as input_file:
    twitter_keys = json.load(input_file)

# try:
# tso = TwitterSearchOrder() # create a TwitterSearchOrder object
# tso.set_keywords(['microsoft', 'windows', 'msft'], or_operator=True) # let's define all words we would like to have a look for
# # tso.set_keywords(['since:2010-12-27','until:2010-12-26'])
# tso.set_language('en') # we want to see German tweets only
# tso.set_include_entities(False) # and don't give us all those entity information
#
# querystr = tso.create_search_url()
# # since=2015-08-31&
# tso.set_search_url(querystr + '&until=2017-07-25')

# it's about time to create a TwitterSearch object with our secret tokens
# ts = TwitterSearch(
#     consumer_key = twitter_keys['consumer_key'],
#     consumer_secret = twitter_keys['consumer_secret'],
#     access_token = twitter_keys['access_token'],
#     access_token_secret = twitter_keys['access_token_secret']
#  )
#
#  # this is where the fun actually starts :)
# i = 0
#
# sleep_for = 60  # sleep for 60 seconds
# last_amount_of_queries = 0  # used to detect when new queries are done
#
# tweets = {}
# for tweet in ts.search_tweets_iterable(tso):
#     tweets.update({i: tweet})
#     print tweets[i]['created_at']
#     # print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
#
#     current_amount_of_queries = ts.get_statistics()[0]
#     if not last_amount_of_queries == current_amount_of_queries:
#         last_amount_of_queries = current_amount_of_queries
#         time.sleep(sleep_for)
#
#     i += 1

# except TwitterSearchException as e: # take care of all those ugly errors if there are some
#     print(e)

results = []

for item in ['microsoft', 'msft', 'windows']:

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(item).setSince("2015-08-31").setUntil("2015-09-30")

    tweet = got.manager.TweetManager.getTweets(tweetCriteria)

    results += tweet

import pickle as pkl
with open('tweet_data.pkl', 'w') as output:
    pkl.dump(results, output)
from nltk import sent_tokenize, word_tokenize

import quandl

with open('/Users/ggao/.quandl_api_key', 'r') as input_file:
    quandl.ApiConfig.api_key = input_file.read()

price_data = quandl.get('EOD/MSFT', start_date="2015-08-31", end_date="2015-09-30")

with open('tweet_data.pkl', 'rb') as input_file:
    tweet_data = pkl.load(input_file)

