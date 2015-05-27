#!/usr/bin/python2.7
# Copyright 2015 Ethan Smith

import ConfigParser
from instagram import client, subscriptions

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

print "Using client id: " + config.get('API', 'client_id')
print "Using secret: " + config.get('API', 'client_secret')
