#!/usr/bin/env python

import json
import webapp2
import logging
from google.appengine.api import memcache
from google.appengine.api import urlfetch


def fetchPostCount(remote=False):
	logging.info('Fetching posts count [%s]', remote)
	count = None
	if (not remote):
		logging.info('Getting data from memcache...')
		count = memcache.get('post_count')
	if count is None:
		logging.debug('Updating from Tumbl API...')
		url = 'http://api.tumblr.com/v2/blog/inspired-ui.com/info?\
api_key=aL7rcud5nU6jHkBPn4GZ4tO9a8pnXgfjbYtXLpSsd6MYFDH7h0'
		result = urlfetch.fetch(url, headers = { 'Cache-Control': 'no-cache,max-age=0', 'Pragma': 'no-cache' })
		if result.status_code == 200:
			data = json.loads(result.content)
			logging.info('Receive data from Tumbl API: %s', data)
			count = data['response']['blog']['posts']
			memcache.set('post_count', count)
		else:
			logging.warning('Failed to get post count from Tumbl API. Default value will be used.')
			count = 400
	logging.info('New post count: %s', count)
	return count


class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/javascript';
		count = fetchPostCount()
		script = 'var postCount = %s;' % count
		self.response.out.write(script)


class UpdateHandler(webapp2.RequestHandler):
	def get(self):
		logging.info('Updating posts count...')
		count = fetchPostCount(True)
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(count)


app = webapp2.WSGIApplication([('/posts', MainHandler), ('/posts/update', UpdateHandler)], debug=True)
