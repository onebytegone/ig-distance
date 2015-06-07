#!/usr/bin/python2.7
# Copyright 2015 Ethan Smith

import ConfigParser
from urllib import urlencode

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

print "Using client id: " + config.get('API', 'client_id')
print "Using access token: " + config.get('API', 'access_token')

client_id = config.get('API', 'client_id')
authorize_url = config.get('API', 'authorize_url')


def get_authorize_url(authorize_url, client_id, redirect_uri):
    client_params = {
        "client_id": client_id,
        "response_type": "token",
        "redirect_uri": redirect_uri
    }
    url_params = urlencode(client_params)
    return "%s?%s" % (authorize_url, url_params)


def getAccessTokenFromUser():
   print "No valid access token."
   print "Please authorize this app at: "
   print get_authorize_url(authorize_url, client_id, config.get('API', 'redirect_uri'))

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
