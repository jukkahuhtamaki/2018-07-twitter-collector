# -*- coding: utf-8 -*-

'''

'''
# # Connect to database
# from pymongo import Connection

# class ProxyDB:
#   connection = None
#   def __init__(self):
#     # Creating a proxy database
#     # Open MongoDB connection
#     connection = Connection()
#     self.tweets = connection.speed.paristweets


from pymongo import MongoClient

class ProxyDB:
  connection = None
  def __init__(self,proxy='local'):
    # Creating a proxy database
    connection = None
    # Open MongoDB connection
    if proxy == 'local':
      # connection = Connection()
      self.tweets = MongoClient().tweets.paristweets
      # self.tweets = connection.tweets.speed.case.consolewars
