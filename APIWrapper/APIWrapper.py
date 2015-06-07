# Copyright 2015 Ethan Smith

class APIWrapper(object):
   """APIWrapper abstracts accessing a RESFUL API"""
   def __init__(self, baseURL, accessToken):
      super(APIWrapper, self).__init__()
      self.baseURL = baseURL
      self.accessToken = accessToken
