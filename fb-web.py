#!/usr/bin/env python
# coding: utf-8

import sys, os.path
#sys.path.append("/home/steve/Desktop/code/py-FaceWall/python-sdk/src/")
#sys.path.append("/home/os2012/work/py-FaceWall/python-sdk/src/")
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
app_id = config.get('facebook','app_id')
app_secret = config.get('facebook','app_secret')
feed_id = config.get('facebook','feed_id')

try:
	proxy_host = config.get('connection','proxy_host')
	proxy_port = config.get('connection','proxy_port')
except ConfigParser.NoOptionError:
	proxy_host = ''
	
try:	
	docroot = config.get('httpd','docroot')
except ConfigParser.NoOptionError:
	exit(1, 'You need to specify docroot in the config file!')	

def debug():
	print '<!--'
	print '##########################################################################################################'
	print '# The posters ID is: ' + unicode(poster_id)
	print '# This is post No: ' + unicode(rand_post) + ' data in post: ' + unicode(post)
	print '##########################################################################################################'
	print '-->'

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
	oauth_access_token = getAccessToken()

	facebook_graph = facebook.GraphAPI(oauth_access_token)
	feed = facebook_graph.get_connections(feed_id, "feed")
	rand_post = random.randint(0, len(feed["data"]) - 1) 
	post = feed["data"][rand_post]

	poster_name = unicode(post['from']['name'])
	poster_id = post['from']['id']
	#profile_picture = "profile_picture=" + poster_picture_url # (dr) not used anywhere
	poster_picture_url = 'http://graph.facebook.com/' + poster_id + '/picture?type=large'
	fetchPosterPicture(poster_picture_url, poster_id)
	fb_data = {
		'poster_id' : poster_id,
		'poster_name' : poster_name,
		'post' : post
	}
	return fb_data
		
	
def getTweets():
	try:
		enable_twitter = config.get('twitter','enable')
		if (enable_twitter):
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
			print(res)
			
			jdict = json.loads(res)
			print(jdict['results'])
			
			rand_tweet = random.randint(0, len(jdict['results']) - 1) 
			tweet = jdict['results'][rand_tweet]
			
			fetchPosterPicture(tweet['profile_image_url'], tweet['from_user_id'])
			tw_data = {
				'poster_id' : tweet['from_user_id'],
				'poster_name' : tweet['from_user'],
				'text' : tweet['text']
			}
			return tw_data
		
	except ConfigParser.NoOptionError:
		enable_twitter = false
	

def fetchPicture(picture_url, poster_id):
	""" Simply fetch a file if it doesn't yet exist and store it under the docroot directory """
	# Fetching Picture of poster
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
	  <title>BEE SECURE On Stéitsch Live FaceBook Wall</title>
	  <meta http-equiv="refresh" content="10" >
	  <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
	  <link rel="stylesheet" type="text/css" href="main.css" >
	</head>

	<body>

	<div id="wrap">
	  <div id="header"><p class="header"><img src="header-logo.png" alt="Logo BEE SECURE" height="47" style="vertical-align: middle">On St&eacute;itsch Live FaceBook Wall</p></div>
	  <br >
	"""
	return html
	
def writeTwHtml(poster_id, poster_name, text):
	""" Write html for a tweet"""
	html = '<div id="twitter" class="norm"><img src="' + unicode(poster_id) + '.jpg" alt="Profile Picture of Poster"' + ' width="100" align="left">'
	html += '<br/>\n'
	html += poster_name + ': '
	html += '\n</div>\n<br/>'
	
	html += '<div id="message" style="margin:0 20% 0 30% " class="header">' + unicode(text) + '</div>\n'
				
def writeFbHtml(poster_id, poster_name, post):		
	""" Write html for facebook"""
	
	html = '<div id="facebook" class="norm"><img src="' + unicode(poster_id) + '.jpg" alt="Profile Picture of Poster"' + ' width="100" align="left">'
	html = html + """    <br >
			"""
	html = html + poster_name + ': '
	#html = html + unicode(poster_name) + u' schréift: '
	html = html + """
	"""
	html = html + """  </div>
	  <br >
	"""

	post_message = post.get('message')
	if post_message == None:
		print 'No message in post :('
		message = "0"
	else:
		#print 'Message in Post: ' + unicode(post_message)
		#message = "message=" + unicode(post_message)
		html = html + '  <div id="message" style="margin:0 20% 0 30% " class="header">' + unicode(post_message) + '</div>'
		#html = html + """
	#"""
		html += "\n"

		post_likes = post.get('likes')
		if post_likes == None:
			#print 'No Likes yet :('
			likes = "0"
			html = html + '    <div id="likes" class="likes"><img src="thumbs-down.png" alt="Like Thumbs-up" height="100" align="top"><br >:(</div>'
			## SEE ABOVE --> Replace with \n ?!
			html = html + """
	</div>
	"""
		else:
			#print 'yay we have ' + unicode(post_likes['count']) + ' likes'
			likes = unicode(post_likes['count'])
			html = html + """
	"""
			html = html + '    <div id="likes" class="likes"><img src="thumbs-up.png" alt="Like Thumbs-up" height="100" align="top"><br >' + unicode(post_likes['count']) + '</div>'
			html = html + """
	</div>
	<br >
	"""
		debug()

	##	html = html + '<div id="footer" class="norm">P.S: Bei Facebook bass de eng Nummer! An zwar: <b>' + unicode(poster_id) + '</b><br >'
	##	html = html + """
	##"""
	##	html = html + '<br >Kee Plang wat di <b>Nummer</b> heescht??? Kee Problem komm bei de <img src="/tmp/header-logo.png" align="middle" height="17"> Stand a kuck der et selwer un.'
	##	html = html + """
	##</div>"""


def writeHtmlFooter(html):
	html += """
		</body>
		</html>
	"""
	local_file = codecs.open('%s/index.html' % docroot, encoding='utf-8', mode="w")
	local_file.write(html)
	local_file.close()

def main():
	html = writeHtmlHeader()
	
	fb_data = getFbPost()
	html += writeFbHtml(**fb_data)
	
	tw_data = getTweets()
	print(tw_data)
	html += writeTwHtml(**tw_data)
		
	writeHtmlFooter(html)
	
	
if __name__ == "__main__":
	main()
