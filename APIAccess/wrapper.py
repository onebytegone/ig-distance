# Copyright 2015 Ethan Smith

class wrapper(object):
   """wrapper abstracts accessing a RESFUL API"""
   def __init__(self, baseURL, accessToken):
      super(wrapper, self).__init__()
      self.baseURL = baseURL
      self.accessToken = accessToken
