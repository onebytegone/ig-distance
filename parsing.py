#!/usr/bin/python2.7
# Copyright 2015 Ethan Smith

import logging
import ConfigParser
import DeepThaw
import os
import itertools

config = ConfigParser.RawConfigParser()
config.read('config.cfg')
logging.basicConfig(level=config.getint('logs', 'level'))

dataStore = DeepThaw.storage('data')

toAnalyze = os.listdir('data')
userGroup = filter(lambda x: x[0] != '.', toAnalyze)
userGroup = filter(lambda x: x != 'summary.json', userGroup)
userGroup = filter(lambda x: x != 'all_comments.json', userGroup)
print userGroup


summary = {}

def getPostsForUser(user):
   return dataStore.fetch([user], 'posts').itervalues().next()['data']

def userInList(user, list):
   return any(x for x in list if x['username'] == user)

def userDidCommentOnPost(user, comments):
   return any(x for x in comments['data'] if x['from']['username'] == user)

def doesUserFollowUser(source, target):
   followsList = dataStore.fetch([source], 'follows').itervalues().next()
   return userInList(target, followsList['data'])

def likesTowardsPostsOf(source, target):
   stats = getPostsForUser(target)

   return reduce(lambda carry, x: carry + (1 if userInList(source, x['likes']['data']) else 0), stats, 0)

def commentsOnPostsOf(source, target):
   stats = getPostsForUser(target)

   return reduce(lambda carry, x: carry + (1 if  userDidCommentOnPost(source, x['comments']) else 0), stats, 0)

def commentsAtUserInPosts(posts, source, target):
   total = 0
   for post in posts:
      allComments = post['comments']['data']
      filteredComments = filter(lambda x: x['from']['username'] == source, allComments)
      total += len(filter(lambda x: '@'+target in x['text'], filteredComments))

   return total

def filterCommentsFrom(comments, source):
   return filter(lambda x: x['from']['username'] == source, comments)

def filterCommentsAtUser(comments, target):
   return len(filter(lambda x: '@'+target in x['text'], comments))

def extractAllComments(group):
   comments = []
   for user in group:
      posts = getPostsForUser(user)
      foundComments = map(lambda x: x['comments']['data'], posts)
      foundComments = list(itertools.chain(*foundComments )) #flatten list
      comments += foundComments
   dataStore.store(comments, [], 'all_comments')


extractAllComments(userGroup)
allComments = dataStore.fetch([], 'all_comments').itervalues().next()
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
      comments = filterCommentsFrom(allComments, user)
      userSummary['numOfCommentsMade'] = len(comments)
      userSummary['commentsToward'][otherUser] = filterCommentsAtUser(comments, otherUser)

   summary[user] = userSummary

dataStore.store(summary, [], 'summary')
