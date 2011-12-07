#!/usr/bin/env python

import json
import webapp2
from google.appengine.api import memcache
from google.appengine.api import urlfetch


def fetchPostCount(remote=False):
		count = None
		if (not remote):
			count = memcache.get('post_count')
		if count is None:
			url = 'http://api.tumblr.com/v2/blog/inspired-ui.com/info?\
api_key=aL7rcud5nU6jHkBPn4GZ4tO9a8pnXgfjbYtXLpSsd6MYFDH7h0'
			result = urlfetch.fetch(url)
			if result.status_code == 200:
				data = json.loads(result.content)
				count = data['response']['blog']['posts']
				memcache.set('post_count', count)
			else:
				count = 300
		return count


class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/javascript';
		count = fetchPostCount()
		script = 'var postCount = %s;' % count
		self.response.out.write(script)


class UpdateHandler(webapp2.RequestHandler):
	def get(self):
		count = fetchPostCount(True);
		self.response.headers['Content-Type'] = 'text/plain';
		self.response.out.write(count)


app = webapp2.WSGIApplication([('/posts', MainHandler), ('/posts/update', UpdateHandler)], debug=True)
