# Copyright 2015 Ethan Smith

from connect import connect as APIConnect

class wrapper(object):
   """wrapper abstracts accessing a RESFUL API"""
   protocol = "http"
   domain = "www.example.com"
   basePath = "v1"
   accessTokenField = "access_token"
   connect = APIConnect()


   def __init__(self, accessToken):
      super(wrapper, self).__init__()
      self.accessToken = accessToken


   def _call(self, segments = [], urlparams = {}, method = "GET"):
      url = self.protocol + '://' + self.domain + '/' + self.basePath
      urlparams[self.accessTokenField] = self.accessToken
      self.connect.call(url, segments, urlparams, method)
