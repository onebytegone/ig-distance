import unittest
from APIConnect import APIConnect

def fun(x):
    return x + 1

class APIConnectTests(unittest.TestCase):
    def testBuildURL(self):
      api = APIConnect()

      # url only
      self.assertEqual(api.buildURL("http://example.com"), "http://example.com")
      self.assertEqual(api.buildURL("http://example.com/"), "http://example.com")

      # url segment only
      self.assertEqual(api.buildURL(
         "http://example.com",
         [ "v1", "/api/" ]
      ), "http://example.com/v1/api")

      # param only
      self.assertEqual(api.buildURL(
         "http://example.com",
         params = {
            "token" : "abcd",
            "details" : 1
         }
      ), "http://example.com?token=abcd&details=1")

      # segment and param
      self.assertEqual(api.buildURL(
         "http://example.com",
         [ "v1", "api" ],
         {
            "token" : "abcd",
            "details" : 1
         }
      ), "http://example.com/v1/api?token=abcd&details=1")
