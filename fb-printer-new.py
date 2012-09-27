#!/usr/bin/env python
# coding: utf-8

import sys, os.path
fb_sdk = os.path.join(os.path.dirname(__file__), 'python-sdk/src/')
sys.path.append(fb_sdk)
import facebook
import urllib, urllib2
import urlparse
import random
import hashlib
import codecs
import ConfigParser
import json

""" Read the config file """
config = ConfigParser.ConfigParser()
config.readfp(open('facebook.cfg'))

try:
	proxy_host = config.get('connection','proxy_host')
	proxy_port = config.get('connection','proxy_port')
except ConfigParser.NoOptionError:
	proxy_host = ''
	
try:
	enable_twitter = config.get('twitter','enable')
	enable_twitter = True if enable_twitter == "true" else False
except ConfigParser.NoOptionError:
	enable_twitter = False
	
try:
	enable_fb = config.get('facebook','enable')
	enable_fb = True if enable_fb == "true" else False
except ConfigParser.NoOptionError:
	enable_fb = False		


def getAccessToken():
	""" Trying to get an access token. Very awkward. """
	oauth_url = 'https://graph.facebook.com/oauth/access_token?'

	oauth_args = {
			'client_id' : app_id,
			'client_secret' : app_secret,
			'grant_type'	: 'client_credentials'
		}
	params = urllib.urlencode(oauth_args)

	if proxy_host:
		proxies = {'http' : '%s:%s' % (proxy_host,proxy_port)}
		proxy_support = urllib2.ProxyHandler(proxies)
		opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=9))
		# (dr) HMPF.. 106 connection timed out
	else:
		opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))	

	urllib2.install_opener(opener)
	req = urllib2.Request(oauth_url,params)
	oauth_response = urllib2.urlopen(req).read()

	try:
	    return urlparse.parse_qs(str(oauth_response))['access_token'][0]
	except KeyError:
	    print('Unable to grab an access token!')
	    exit()


def getFbPost():
	app_id = config.get('facebook','app_id')
	app_secret = config.get('facebook','app_secret')
	feed_id = config.get('facebook','feed_id')
	
	oauth_access_token = getAccessToken()

	facebook_graph = facebook.GraphAPI(oauth_access_token)
	feed = facebook_graph.get_connections(feed_id, "feed")
	post = feed["data"][0]

	poster_name = unicode(post['from']['name'])
	poster_id = post['from']['id']
	#profile_picture = "profile_picture=" + poster_picture_url 
	#poster_picture_url = 'http://graph.facebook.com/' + poster_id + '/picture?type=large'
	#fetchPosterPicture(poster_picture_url, poster_id)
	
	#html += '<div style="float:left; "><img src="' + 'file://' + '/tmp/' + poster_id + '.jpg"' + ' width="100" align="left"></div>'
	#html += '<br />\n'
	#html += '<font size="3" face="arial" color="black"> ' + unicode(poster_name) + u' schréift: </font>'
	#html += '<br />\n'
	
	post_message = post.get('message')
	post_hash = hashlib.sha224(repr(post_message)).hexdigest()
	if post_message == None:
		#print 'No message in post :('
		message = "0"
	elif os.path.exists('/tmp/' + post_hash + '.txt') == False:
		""" Don't print if we already printed this (at least until /tmp gets cleaned up ;)) """		
		local_file = codecs.open('/tmp/' + post_hash + '.txt', encoding='utf-8', mode="w")
		local_file.write(post_message)
		local_file.close()
		
		post_likes = post.get('likes')
		if post_likes == None:
			likes = "0"
		else:
			likes = unicode(post_likes['count'])
			#html += '<div><img src="file:///tmp/thumbs-up.png" width="100" align="absmiddle"> <font size="7" face="arial" color="#5a749f">' + unicode(post_likes['count']) + '</font></div>\n'
			
		if ( len(post_message) > 324 ):
			message = post_message[0:324] + u'...'
		else:
			message = post_message
			
		message = message + u' \n'
		message = message + u'www.bee-secure.lu/beefair\n'
		message = message + u' \n'
		message = message + u'Live vu FaceBook vum: ' + poster_name
		print message
		return message
	else:
		print("message already printed")
		exit(0)

	
def getTweets():
	search_term = config.get('twitter','search')
	url = 'http://search.twitter.com/search.json'
	search_args = {
		'q' : search_term,
		'result_type' : 'mixed',
		'show_user' : True
		#'include_entities' : True	# includes info about hashtags, etc
		}
	search_params = urllib.urlencode(search_args)
	res = urllib2.urlopen(url, search_params).read()
	jdict = json.loads(res)
	
	rand_tweet = random.randint(0, len(jdict['results']) - 1) 
	tweet = jdict['results'][rand_tweet]
	#fetchPicture(tweet['profile_image_url'], tweet['from_user_id_str'])
	
	post_message = tweet['text']
	post_hash = hashlib.sha224(repr(post_message)).hexdigest()
	if post_message == None:
		#print 'No message in post :('
		message = "0"
	elif os.path.exists('/tmp/' + post_hash + '.txt') == False:
		""" Don't print if we already printed this (at least until /tmp gets cleaned up ;)) """		
		local_file = codecs.open('/tmp/' + post_hash + '.txt', encoding='utf-8', mode="w")
		local_file.write(post_message)
		local_file.close()
		
		if ( len(post_message) > 324 ):
			message = post_message[0:324] + u'...'
		else:
			message = post_message
			
		message = message + u' \n'
		message = message + u'www.bee-secure.lu/beefair\n'
		message = message + u' \n'
		message = message + u'Live vun Twitter vum: @' + tweet['from_user']
		print message
		print(tweet['from_user'],tweet['from_user_id_str'],tweet['text'])
		return message
	else:
		print("message already printed")
		exit(0)
		
	
def fetchPicture(picture_url, poster_id):
	""" Simply fetch a file if it doesn't yet exist and store it under the docroot directory """
	# Fetching Picture of poster
	if os.path.exists('/tmp/' + poster_id + '.jpg') == False:
		f_url = urllib2.urlopen(picture_url)
		local_file = open('/tmp/' + poster_id + '.jpg', "w")
		local_file.write(f_url.read())
		local_file.close()


def writeMessageToFile(message):
	local_file = codecs.open('print.txt', encoding='utf-8', mode="w")
	local_file.write(message)
	local_file.close()


def main():
	
	# Twitter or Facebook, what should we hit?
	rand = random.randint(1,2)
		
	if enable_fb != False and (enable_twitter == False or rand == 1):
		message = getFbPost()
		
	if enable_twitter != False and (enable_fb == False or rand == 2):
		message = getTweets()
		
	writeMessageToFile(message)
	
	
if __name__ == "__main__":
	main()
