import requests
# from requests_oauthlib import OAuth1
from requests.exceptions import ConnectionError

import urllib

# import pandas as pd
import simplejson as json

import time, datetime

from pprint import pprint

with open('keychain.json') as f:
  keychain = json.load(f)

# Authenticating to Twitter API
from requests_oauthlib import OAuth1

def get_oauth():
  oauth = OAuth1(keychain['CONSUMER_KEY'],
              client_secret=keychain['CONSUMER_SECRET'],
              resource_owner_key=keychain['ACCESS_TOKEN'],
              resource_owner_secret=keychain['ACCESS_TOKEN_SECRET'])
  return oauth

auth = get_oauth()


'''
Using MongoDB to manage tweet data
'''
# Setting up proxy database for the tweets
from proxydb import ProxyDB
db = ProxyDB()

class Tweet:
  def __init__(self,db,id,data,search_term,collection):
    self.db = db
    self.id = id
    self.data = data
    self.data['tweetcollectionname'] = collection
    self.data['searchterm'] = search_term

  def save(self):
    # Updating DB
    tweet_in_db = self.db.tweets.find_one({'id': self.id})
    if not tweet_in_db:
      # Insert to database
      self.db.tweets.insert(self.data)
      return True
    # Tweet already in DB
    return False

def sleep():
  print("%s: The script now sleeps for 15 minutes before fetching more results..." % (datetime.datetime.now().isoformat()))
  time.sleep(300) # 300 sec = 5 min
  print("...5 minutes gone...")
  time.sleep(300) # 300 sec = 5 min
  print("...10 minutes gone...")
  time.sleep(300) # 300 sec = 5 min
  print("...15 minutes gone...")
  #  time.sleep(300) # 300 sec = 5 min
  print("...OK! Will now continue.")

auth = get_oauth()

cursor = -1
listmembers = list()
# fname='/home/ec2-user/2014/04-euvaalit/data/01-seeddata/candidates.csv'

# listmembers=pd.io.parsers.read_csv(fname)

print(listmembers)

while True:

  # with open('data/02-refined/listmembers.json','r') as f:
  #   listmembers = json.load(f)

  #   # pprint(r.json())

  # print 'Ok, we have the users listed. Let\'s collect their recent tweets.'

  url_next_template = 'https://api.twitter.com/1.1/search/tweets.json?include_entities=1&result_type=recent&count=100&%s'

  request_count = 0
  for hashtag in ['#pymongo', '#mongoDB']:
    # print url_next % user['screen_name']
    tweets = dict()
    # search_param = {'q' : 'from:%s' % user['screen_name']}
    # screen_name = user
    search_param = {'q' : '%s' % (hashtag)}
    print('Params for the next query: %s' % urllib.parse.urlencode(search_param))
    url_next = url_next_template % urllib.parse.urlencode(search_param)
    try:
      while True:
        # url_next = url_next_template % user['screen_name']
        # print url_next
        if request_count == 10:
          check_api_status()
          request_count = 0

        try:
          r = requests.get(url=url_next, auth=get_oauth())
        except ConnectionError as e:
          print('Error when fetching next URL: \n', e)
          sleep()
          continue

        request_count = request_count+1
        print('Requests after the latest status check: %s' % request_count)
        # ids = dict()
        for tweet in r.json()['statuses']:
          tweets[tweet['id']] = tweet
          tweet_in_db = Tweet(db,tweet['id'],tweet,search_param['q'],'collection:speed.gametweets')
          tweet_in_db.save()
          # ids[status['id_str']] = 1
        # pprint(sorted(ids))
        # Next set of tweets
        pprint(r.json()['search_metadata'])
        url_next = 'https://api.twitter.com/1.1/search/tweets.json%s' % r.json()['search_metadata']['next_results']
        print('Tweets collected: %s' % len(tweets))
        time.sleep(10)
        # with open('temp/example_with_requests.json', 'w') as f:
        #       json.dump(r.json(),f,indent=1)
    except KeyError as e:
      print(e)
      print('Collected %s tweets for %s' % (len(tweets),criteria))
