# Copyright 2015 Ethan Smith

import os, errno
import json
import datetime

class storage(object):
   """wrapper abstracts storing data"""

   def __init__(self, basePath):
      self.basePath = basePath

   def store(self, jsonMappable, identifiers, name):
      package = self.fetch(identifiers, name)
      package[str(datetime.datetime.now())] = jsonMappable

      string = json.dumps(package, indent=4, separators=(',', ': '))

      path = self.makePath(identifiers, name)

      with open(path, "w") as outfile:
         outfile.write(string)

   def fetch(self, identifiers, name):
      path = self.makePath(identifiers, name)
      if os.path.isfile(path):
         with open(path, "r") as infile:
            contents = infile.read()
            if contents == '':
               return {}
            return json.loads(contents)
      return {}

   def makePath(self, identifiers, name):
      directory = self.storageDirectory(identifiers)
      mkdir(directory)
      return directory + '/' + name + '.json'

   def storageDirectory(self, identifiers):
      return os.path.join(self.basePath, *identifiers)

def mkdir(path):
   try:
      os.makedirs(path)
   except OSError as exc:
      if exc.errno == errno.EEXIST and os.path.isdir(path):
         pass
      else: raise
