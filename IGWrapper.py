# Copyright 2015 Ethan Smith

import APIAccess

class IGWrapper(APIAccess.wrapper):
   """An APIWrapper for Instagram"""
   authorize_url = 'https://api.instagram.com/oauth/authorize'
   protocol = "https"
   domain = "api.instagram.com"
   basePath = "v1"
   accessTokenField = "access_token"

   @staticmethod
   def get_authorize_url(client_id, redirect_uri):
      client_params = {
         'client_id': client_id,
         'response_type': 'token',
         'redirect_uri': redirect_uri
      }
      url_params = urlencode(client_params)
      return '%s?%s' % (authorize_url, url_params)
