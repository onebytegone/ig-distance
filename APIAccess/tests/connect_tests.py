import unittest
from connect import connect as APIConnect

def fun(x):
    return x + 1

class connecttests(unittest.TestCase):
    def testBuildURL(self):
      connect = APIConnect()

      # url only
      self.assertEqual(connect.buildURL("http://example.com"), "http://example.com")
      self.assertEqual(connect.buildURL("http://example.com/"), "http://example.com")

      # url segment only
      self.assertEqual(connect.buildURL(
         "http://example.com",
         [ "v1", "/api/" ]
      ), "http://example.com/v1/api")

      # param only
      self.assertEqual(connect.buildURL(
         "http://example.com",
         params = {
            "token" : "abcd",
            "details" : 1
         }
      ), "http://example.com?token=abcd&details=1")

      # segment and param
      self.assertEqual(connect.buildURL(
         "http://example.com",
         [ "v1", "api" ],
         {
            "token" : "abcd",
            "details" : 1
         }
      ), "http://example.com/v1/api?token=abcd&details=1")
