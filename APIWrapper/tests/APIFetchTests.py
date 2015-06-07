import unittest
from APIFetch import APIFetch

def fun(x):
    return x + 1

class APIFetchTests(unittest.TestCase):
    def testBuildURL(self):
      fetch = APIFetch()

      # url only
      self.assertEqual(fetch.buildURL("http://example.com"), "http://example.com")
      self.assertEqual(fetch.buildURL("http://example.com/"), "http://example.com")

      # url segment only
      self.assertEqual(fetch.buildURL(
         "http://example.com",
         [ "v1", "/api/" ]
      ), "http://example.com/v1/api")

      # param only
      self.assertEqual(fetch.buildURL(
         "http://example.com",
         params = {
            "token" : "abcd",
            "details" : 1
         }
      ), "http://example.com?token=abcd&details=1")

      # segment and param
      self.assertEqual(fetch.buildURL(
         "http://example.com",
         [ "v1", "api" ],
         {
            "token" : "abcd",
            "details" : 1
         }
      ), "http://example.com/v1/api?token=abcd&details=1")
