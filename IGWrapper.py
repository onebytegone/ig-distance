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

   def userInfo(self, user_id = 'self'):
      return self._call([ 'users', user_id ])

   def follows(self, user_id = 'self'):
      return self._call([ 'users', user_id, 'follows' ])

   def followedBy(self, user_id = 'self'):
      return self._call([ 'users', user_id, 'followed-by' ])

   def posts(self, user_id = 'self'):
      return self._call([ 'users', user_id, 'media', 'recent' ])

   def userSearch(self, username):
      return self._call([ 'users', 'search' ], urlparams = {'q': username})

   def getPaginationURL(self, data):
      if 'pagination' in data and 'next_url' in data['pagination']:
         return data['pagination']['next_url']
      return None

   def mergeFromPagination(self, oldData, newData):
      mergedData = newData
      mergedData['data'] = oldData['data']+newData['data']
      return mergedData
