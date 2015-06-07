#!/usr/bin/python2.7
# Copyright 2015 Ethan Smith

import logging
import ConfigParser
from IGWrapper import IGWrapper
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

access_token = retrieveAccessToken()
