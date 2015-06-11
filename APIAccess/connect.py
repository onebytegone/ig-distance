# Copyright 2015 Ethan Smith

import logging
import urllib2
import json
from urllib import urlencode

class connect(object):
   """connect abstracts calls to endpoints"""
   def __init__(self):
      super(connect, self).__init__()

   def call(self, baseurl, segments, urlparams = [], method = "GET"):
      url = self.buildURL(baseurl, segments, urlparams)
      logging.info('Accessing: ' + method + ' ' + url)
      req = urllib2.Request(url)
      req.get_method = lambda: method
      response = urllib2.urlopen(req)
      data = response.read()
      return json.loads(data)

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
