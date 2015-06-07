#!/usr/bin/python2.7
# Copyright 2015 Ethan Smith

import ConfigParser
from instagram import client, subscriptions, InstagramAPI

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

print "Using client id: " + config.get('API', 'client_id')
print "Using secret: " + config.get('API', 'client_secret')
print "Using access token: " + config.get('API', 'access_token')

unauthenticated_api = InstagramAPI(
   client_id=config.get('API', 'client_id'),
   client_secret=config.get('API', 'client_secret'),
   redirect_uri=config.get('API', 'redirect_uri'))

def connectToAPI(access_token):
   if not access_token:
      access_token = exchangeCodeForToken(getAccessCodeFromUser())

   return client.InstagramAPI(access_token=access_token, client_secret=config.get('API', 'client_secret'))

def exchangeCodeForToken(access_code):
   try:
      access_token, user_info = unauthenticated_api.exchange_code_for_access_token(access_code)
      if not access_token:
         print 'Could not get access token.'
         return exchangeCodeForToken(getAccessCodeFromUser())
      config.set('API', 'access_token', access_token)
      print access_token
      return access_token
   except Exception as e:
      print(e)
      return exchangeCodeForToken(getAccessCodeFromUser())


def getAccessCodeFromUser():
   print "No valid access token."
   print "Please authorize this app at: " + unauthenticated_api.get_authorize_url()
   return raw_input('Enter access code: ')

api = connectToAPI(config.get('API', 'access_token'))
