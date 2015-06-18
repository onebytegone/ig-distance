# Copyright 2015 Ethan Smith

import logging
import urllib2
import json
from urllib import urlencode
import ssl

class connect(object):
   """connect abstracts calls to endpoints"""
   def __init__(self):
      super(connect, self).__init__()

   def call(self, baseurl, segments, urlparams = [], method = "GET"):
      url = self.buildURL(baseurl, segments, urlparams)
      logging.info('Accessing: ' + method + ' ' + url)
      req = urllib2.Request(url)
      req.get_method = lambda: method
      data = "{}"

      for attempt in range(3):
         try:
            response = urllib2.urlopen(req, timeout = 2)
            data = response.read()
         except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
         except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
         except ssl.SSLError, e:
            print 'SSLError = ' + str(e.reason)
         else:
            break

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
