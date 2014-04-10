import requests
from requests_oauthlib import OAuth1
from pprint import pprint

CONSUMER_KEY = '<consumer_key>'
CONSUMER_SECRET = '<consumer_secret>'
ACCESS_TOKEN = '<access_token>'
ACCESS_TOKEN_SECRET = '<access_token_secret>'

"""
  Twitter URLs used for API endpoints, part of the REST API. Streaming API is
    very different and not covered here. New version of the API is '1.1' (as
    seen in the URLs), but many of the API version 1 calls still work. Rate
    limit information: https://dev.twitter.com/docs/rate-limiting/1.1

  LOOKUP_URL - Look up profile information for users. Used by apps to get
               follower information, but used here to just pull profile info.
               You can provide a list of up to 100 screen names and api will
               return results for all users found. The limitation here is that
               nothing is returned for screen names not found or suspended, so
               a diff needs to be performed between the lists.

               Request URL: https://api.twitter.com/1.1/users/lookup.json
               Docs: https://dev.twitter.com/docs/api/1.1/get/users/lookup

  SHOW_URL - Show profile information for a specific user and returns error
             code information for users not found. Exactly like lookup but
             returns individual user based info, so it will return error code
             information for users not found instead of leaving them out of
             the results.

             Request URL: https://api.twitter.com/1.1/users/show.json
             Docs: https://dev.twitter.com/docs/api/1.1/get/users/show

  SEARCH_URL - Search for a user based on query information. This will return
               a list of potential matches in order of similarity to the query
               parameters. Useful for searching for screen names when the
               exact name or user id is unknown

               Request URL: https://api.twitter.com/1.1/users/search.json
               Docs: https://dev.twitter.com/docs/api/1.1/get/users/search

  Error codes:
      34 - User does not exist/unregistered. Also returned on lookup if no
             screen names return any results
      64 - Account is suspended, additional information is not avaliable

      Docs: https://dev.twitter.com/docs/error-codes-responses

  Twitter also has a number of reserved account that still have information
    listed through searches for people who registered the account before
    they became reserved. Examples are 'blog', 'all', 'activity'.
    Full list: https://dev.twitter.com/docs/api/1.1/get/help/configuration

  API docs: https://dev.twitter.com/docs/api/1.1
"""
LOOKUP_URL = 'https://api.twitter.com/1.1/users/lookup.json'
SHOW_URL = 'https://api.twitter.com/1.1/users/show.json'
SEARCH_URL = 'https://api.twitter.com/1.1/users/search.json'

auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
session = requests.Session()
session.auth = auth

# if 'errors' in response and response['errors'][0]['code'] == 34:
#     print response

print "Basic lookup for a single user: neworganizing"
print "---------------------------------------------"
params = {'screen_name': 'neworganizing'}
response = session.request('GET', LOOKUP_URL, params=params).json()
pprint(response)

print "\nMulti-user lookup: neworganizing, noitoolbox, doritosloaded"
print "---------------------------------------------------------"
params = {'screen_name': 'neworganizing,noitoolbox,doritosloaded'}
response = session.request('GET', LOOKUP_URL, params=params).json()
pprint(response)

print "\nMulti-user lookup: neworganizing, _a, doritosloaded, lkjawer9"
print "'_a' is a suspended account, 'lkjawer9' is not a registered account"
print "-------------------------------------------------------------------"
params = {'screen_name': 'neworganizing,_a,doritosloaded,lkjawer9'}
response = session.request('GET', LOOKUP_URL, params=params).json()
pprint(response)

print "\nSingle user 'show': neworganizing"
print "-----------------------------------"
params = {'screen_name': 'neworganizing'}
response = session.request('GET', SHOW_URL, params=params).json()
pprint(response)

print "\nSingle user show for a suspended account: _a"
print "----------------------------------------------"
params = {'screen_name': '_a'}
response = session.request('GET', SHOW_URL, params=params).json()
pprint(response)

print "\nSingle user show for an unregistered account: lkjawer9"
print "--------------------------------------------------------"
params = {'screen_name': 'lkjawer9'}
response = session.request('GET', SHOW_URL, params=params).json()
pprint(response)

print "\nExample search for 'Senator Chuck Grassley'"
print "---------------------------------------------"
params = {'q': 'Senator Chuck Grassley', 'page': '1', 'count': '5'}
response = session.request('GET', SEARCH_URL, params=params).json()
pprint(response)

print "\nSearch for 'Vincent DeMarco Sheriff Suffolk County'"
print "-----------------------------------------------------"
params = {'q': 'Vincent DeMarco Sheriff Suffolk County', 'page': '1', 'count': '5'}
response = session.request('GET', SEARCH_URL, params=params).json()
pprint(response)
