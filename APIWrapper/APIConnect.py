# Copyright 2015 Ethan Smith

import urllib2
from urllib import urlencode

class APIConnect(object):
   """APIConnect abstracts calls to endpoints"""
   def __init__(self, baseurl = ""):
      super(APIConnect, self).__init__()
      self.baseurl = baseurl

   def call(self, segments, urlparams = [], method = "GET"):
      pass

   def buildURL(self, base, segments = [], params = {}):
      url = base.rstrip('/')

      # generate url segments
      if len(segments) > 0:
         sanitizedSegments = map(lambda x: x.strip('/'), segments)
         url += '/' + '/'.join(sanitizedSegments)

      # generate url params
      if len(params) > 0:
         url += '?' + urlencode(params)

      return url
