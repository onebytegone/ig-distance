#!/usr/bin/python2.7
# Copyright 2015 Ethan Smith

import logging
import ConfigParser
import DeepThaw
import os

config = ConfigParser.RawConfigParser()
config.read('config.cfg')
logging.basicConfig(level=config.getint('logs', 'level'))

dataStore = DeepThaw.storage('data')

toAnalyze = os.listdir('data')
userGroup = filter(lambda x: x[0] != '.', toAnalyze)
print userGroup


summary = {}

def userInList(user, list):
   return any(x for x in list if x['username'] == user)

def userDidCommentOnPost(user, comments):
   return any(x for x in comments['data'] if x['from']['username'] == user)

def doesUserFollowUser(source, target):
   followsList = dataStore.fetch([source], 'follows').itervalues().next()
   return userInList(target, followsList['data'])

def likesTowardsPostsOf(source, target):
   postList = dataStore.fetch([target], 'posts').itervalues().next()
   stats = postList['data']

   return reduce(lambda carry, x: carry + (1 if userInList(source, x['likes']['data']) else 0), stats, 0)

def commentsOnPostsOf(source, target):
   postList = dataStore.fetch([target], 'posts').itervalues().next()
   stats = postList['data']

   return reduce(lambda carry, x: carry + (1 if  userDidCommentOnPost(source, x['comments']) else 0), stats, 0)

def commentsAtUserInPosts(posts, source, target):
   total = 0
   for post in posts:
      allComments = post['comments']['data']
      filteredComments = filter(lambda x: x['from']['username'] == source, allComments)
      total += len(filter(lambda x: '@'+target in x['text'], filteredComments))

   return total

def commentsAtUser(group, source, target):
   total = 0
   for bystander in group:
      postList = dataStore.fetch([bystander], 'posts').itervalues().next()
      posts = postList['data']
      total += commentsAtUserInPosts(posts, source, target)

   return total


for user in userGroup:
   print 'Parsing user: ' + user
   otherUsers = filter(lambda x: x != user, userGroup)

   userSummary = {
      'follows': {},
      'likesToward': {},
      'commentsOnPosts': {},
      'commentsToward': {}
   }

   userFollowsInfo = {}
   for otherUser in otherUsers:
      userSummary['follows'][otherUser] = doesUserFollowUser(user, otherUser)
      userSummary['likesToward'][otherUser] = likesTowardsPostsOf(user, otherUser)
      userSummary['commentsOnPosts'][otherUser] = commentsOnPostsOf(user, otherUser)
      userSummary['commentsToward'][otherUser] = commentsAtUser(userGroup, user, otherUser)

   summary[user] = userSummary

dataStore.store(summary, [], 'summary')
