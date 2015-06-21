#!/usr/bin/python2.7
# Copyright 2015 Ethan Smith

import logging
import ConfigParser
from IGWrapper import IGWrapper
import DeepThaw
from urllib import urlencode



config = ConfigParser.RawConfigParser()
config.read('config.cfg')
logging.basicConfig(level=config.getint('logs', 'level'))

print "Using client id: " + config.get('API', 'client_id')
print "Using access token: " + config.get('API', 'access_token')

client_id = config.get('API', 'client_id')


def getAccessTokenFromUser():
   print "No valid access token."
   print "Please authorize this app at: "
   print IGWrapper.get_authorize_url(client_id, config.get('API', 'redirect_uri'))

   hasAuthorized = 'n'
   while hasAuthorized.lower() == 'n':
      hasAuthorized = raw_input('Have you authorized me? (y/n) ')

   return raw_input('Enter access token: ')


def retrieveAccessToken():
   access_token = config.get('API', 'access_token')
   if not access_token:
      access_token = getAccessTokenFromUser()
      config.set('API', 'access_token', access_token)

   return access_token


def queryForUserID(username):
   response = api.userSearch(username)
   users = response['data']
   options = map(lambda x: '"' + x['username'] + '" (' + x['full_name'] + ', ' + x['id'] + ')', users)
   print 'Which user are you referring to: (given: ' + username + ')'
   for index, item in enumerate(options):
      print str(index+1) + '. ' + item
   select = raw_input('Which user [1-' + str(len(options)) + ']: ')

   parsed = int(select.strip())
   #TODO: validate response
   user = users[parsed - 1]
   return user['id']


def callAPI(username, userID, endpoint, file):
   data = getattr(api, endpoint)(userID)
   dataStore.store(data, [username], file)

def fetchPosts(username, userID):
   data = api.posts(userID)

   posts = data['data']
   fullPosts = []
   for post in posts:
      postID = post['id']

      if post['comments']['count'] != len(post['comments']['data']):
         post['all_comments'] = api.commentsForPost(postID)['data']
      else:
         post['all_comments'] = post['comments']['data']

      if post['likes']['count'] != len(post['likes']['data']):
         post['all_likes'] = api.likesForPost(postID)['data']
      else:
         post['all_likes'] = post['likes']['data']

      fullPosts.append(post)

   dataStore.store(fullPosts, [username], 'posts')


def storeUser(username):
   userID = queryForUserID(username)
   callAPI(username, userID, 'userInfo', 'userinfo')
   callAPI(username, userID, 'follows', 'follows')
   callAPI(username, userID, 'followedBy', 'followed-by')
   fetchPosts(username, userID)


access_token = retrieveAccessToken()
api = IGWrapper(access_token)
dataStore = DeepThaw.storage('data')
user = raw_input('Which user to fetch data for: ')
storeUser(user)
