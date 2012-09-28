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
	docroot = config.get('httpd','docroot')
	if docroot[-1] != '/':
		docroot += '/'
except ConfigParser.NoOptionError:
	exit(1, 'You need to specify docroot in the config file!')	
	
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
	app_id = config.get('facebook','app_id')
	app_secret = config.get('facebook','app_secret')

	oauth_args = {
			'client_id' : app_id,
			'client_secret' : app_secret,
			'grant_type'	: 'client_credentials'
		}
	params = urllib.urlencode(oauth_args)
	oauth_response = urllib2.urlopen(oauth_url,params).read()

	try:
	    return urlparse.parse_qs(str(oauth_response))['access_token'][0]
	except KeyError:
	    print('Unable to grab an access token!')
	    exit()
	    
	    
def restRequest():
	"""
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
	"""


def getFbPost():
	""" Select a random facebook post! """
	feed_id = config.get('facebook','feed_id')
	oauth_access_token = getAccessToken()

	facebook_graph = facebook.GraphAPI(oauth_access_token)
	feed = facebook_graph.get_connections(feed_id, "feed")
	rand_post = random.randint(0, len(feed["data"]) - 1) 
	post = feed["data"][rand_post]

	poster_name = unicode(post['from']['name'])
	poster_id = post['from']['id']
	poster_picture_url = 'https://graph.facebook.com/' + poster_id + '/picture?type=large'
	fetchPicture(poster_picture_url, poster_id)
	
	html = '<div id="facebook" class="sm">'
	html += '<div id="fb_poster" class="norm"><img src="' + unicode(poster_id) + '.jpg" alt="Profile Picture of Poster"' + ' width="100" align="left" style="margin-right:10px;">'
	html += poster_name + ': \n'
	html += '</div>\n'
	
	post_message = post.get('message')
	if post_message == None:
		print 'No message in post :('
		message = "0"
	else:
		html = html + '<div id="fb_message" class="header message">' + unicode(post_message) + '</div>\n'
		post_likes = post.get('likes')
		if post_likes == None:
			likes = "0"
			html += '<div id="likes" class="likes"><img src="thumbs-down.png" alt="Like Thumbs-up" height="100" align="top"> :(</div>'
		else:
			likes = unicode(post_likes['count'])
			html = html + '<div id="likes" class="likes"><img src="thumbs-up.png" alt="Like Thumbs-up" height="100" align="top"><br >' + unicode(post_likes['count']) + '</div>\n'
			
	html += '</div>\n'
	print('Facebook:',poster_name,poster_id,post_message)	
	return html
	
	
def getTweets():
	""" Select a random tweet from a search"""
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
	
	fetchPicture(tweet['profile_image_url'], tweet['from_user_id_str'])
	
	""" Write html for a tweet"""
	html = '<div id="twitter" class="sm">'
	html += '<div id="tw_poster" class="norm"><img src="' + unicode(tweet['from_user_id_str']) + '.jpg" alt="Profile Picture of Poster"' + ' width="100" align="left" style="margin-right:10px;">'
	html += '<br/>\n'
	html += '@' + tweet['from_user'] + ': '
	html += '\n</div>\n<br/>'

	html += '<div id="tw_message" class="header message">' + unicode(tweet['text']) + '</div>\n'
	html += '</div>\n'
	
	print('Twitter:',tweet['from_user'],tweet['from_user_id_str'],tweet['text'])
	return html
		
	
def fetchPicture(picture_url, poster_id):
	""" Simply fetch a file if it doesn't yet exist and store it under the docroot directory """
	if os.path.exists(docroot + poster_id + '.jpg') == False:
		f_url = urllib2.urlopen(picture_url)
		local_file = open(docroot + poster_id + '.jpg', "w")
		local_file.write(f_url.read())
		local_file.close()
		
			
def writeHtmlHeader():
	""" Generating HTML Headers """
	html = u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
		   "http://www.w3.org/TR/html4/loose.dtd">
	<html>
	<head>
	  <title>BEE SECURE On Stéitsch Live FaceBook & Twitter Wall</title>
	  <meta http-equiv="refresh" content="10" >
	  <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
	  <link rel="stylesheet" type="text/css" href="main.css" >
	</head>

	<body>

	<div id="wrap">
	  <div id="header"><p class="header"><img src="header-logo.png" alt="Logo BEE SECURE" height="47" style="vertical-align: middle">On St&eacute;itsch Live FaceBook & Twitter Wall</p></div>
	  <br >
	"""
	return html



def writeHtmlFooter(html):
	html += '\n</div>\n</body>\n</html>\n'
	local_file = codecs.open('%s/index.html' % docroot, encoding='utf-8', mode="w")
	local_file.write(html)
	local_file.close()


def main():
	html = writeHtmlHeader()
	
	if enable_fb != False:
		html += getFbPost()
		
	if enable_twitter != False:
		html += getTweets()
		
	writeHtmlFooter(html)
	
	
if __name__ == "__main__":
	main()
