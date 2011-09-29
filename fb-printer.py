#!/usr/bin/env python
# coding: utf-8

import sys
#sys.path.append("/Users/steve/Desktop/code/python-sdk/src/")
sys.path.append("/home/steve/Desktop/code/python-sdk/src/")
import facebook
import urllib
import urlparse
import subprocess
import random
import os.path
import hashlib
import codecs

def debug():
	print '<!--'
	print '##########################################################################################################'
	print '# The posters ID is: ' + unicode(poster_id) + ' post hash: ' + post_hash
	print '# This is the latest post, data in post: ' + unicode(post)
	print '##########################################################################################################'
	print '-->'


html = """<html>  
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
</head>
<body>

<br />
"""

#html = '<!-- Evil hack to get it working -->'

# Parameters of your app and the id of the profile you want to mess with.
FACEBOOK_APP_ID     = ''
FACEBOOK_APP_SECRET = ''

# Trying to get an access token. Very awkward.
oauth_args = dict(client_id     = FACEBOOK_APP_ID,
                  client_secret = FACEBOOK_APP_SECRET,
                  grant_type    = 'client_credentials')
oauth_curl_cmd = ['curl',
                  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
oauth_response = subprocess.Popen(oauth_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0]

try:
    oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
except KeyError:
    print('Unable to grab an access token!')
    exit()

facebook_graph = facebook.GraphAPI(oauth_access_token)

feed = facebook_graph.get_connections("205667706145726", "feed")

post = feed["data"][0]

poster_name = unicode(post['from']['name'])
poster_id = post['from']['id']
poster_picture_url = 'http://graph.facebook.com/' + poster_id + '/picture?type=large'
profile_picture = "profile_picture=" + poster_picture_url

# Fetching Picture of poster
if os.path.exists('/tmp/' + poster_id + '.jpg') == False:
	f_url = urllib.urlopen(poster_picture_url)
	local_file = open('/tmp/' + poster_id + '.jpg', "w")
	local_file.write(f_url.read())
	local_file.close()
html = html + '<div style="float:left; "><img src="' + 'file://' + '/tmp/' + poster_id + '.jpg"' + ' width="100" align="left"></div>'
html = html + """<br />
"""
html = html + '<font size="3" face="arial" color="black"> ' + unicode(poster_name) + u' schréift: </font>'
html = html + """<br />
"""

post_message = post.get('message')
post_hash = hashlib.sha224(repr(post_message)).hexdigest()
if post_message == None:
	#print 'No message in post :('
	message = "0"
elif os.path.exists('/tmp/' + post_hash + '.txt') == False:
	#print 'Message in Post: ' + unicode(post_message)
	#message = poster_name + " - " + unicode(post_message)
	#print message
	local_file = codecs.open('/tmp/' + post_hash + '.txt', encoding='utf-8', mode="w")
	local_file.write(post_message)
	local_file.close()
	html = html + '<div><font size="10" face="arial" color="black">' + unicode(post_message) + '</font></div>'
	html = html + """
	"""

	post_likes = post.get('likes')
	if post_likes == None:
		#print 'No Likes yet :('
		likes = "0"
	else:
		#print 'yay we have ' + unicode(post_likes['count']) + ' likes'
		likes = unicode(post_likes['count'])
		html = html + '<div><img src="file:///tmp/thumbs-up.png" width="100" align="absmiddle"> <font size="7" face="arial" color="#5a749f">' + unicode(post_likes['count']) + '</font></div>'
		html = html + """
		"""
	debug()
	if ( len(post_message) > 324 ):
		message = post_message[0:324] + u'...'
	else:
		message = post_message
	message = message + u' \n'
	message = message + u'www.bee-secure.lu/saferinternet\n'
	message = message + u' \n'
	message = message + u'Live vu FaceBook vum: ' + poster_name
	print message

##	html = html + '<br />'
##	html = html + """
##	"""
##	html = html + '<div><font size="3" face="arial" color="black">P.S: Bei Facebook bas de eng Nummer! An zwar: <b>' + unicode(poster_id) + '</b><br />'
##	html = html + """
##	"""
##	html = html + '<br />Kee Plang wat di <b>Nummer</b> heescht??? Kee Problem www.beesecure.lu/facebook</font></div>'
##	html = html + """
##	"""
	local_file = codecs.open('printer.html', encoding='utf-8', mode="w")
	local_file.write(html)
	local_file.close()
	local_file = codecs.open('print.txt', encoding='utf-8', mode="w")
	local_file.write(message)
	local_file.close()

#	post_picture = post.get('picture')
#	if post_picture == None:
		#print 'No pics yet :('
#		picture = "picture=0"
#	else:
		#print 'yay we have pics at ' + post_picture
#		file_hash = hashlib.sha224(post_picture).hexdigest()
#		if os.path.exists('/tmp/' + file_hash + '.jpg') == False:
			# Fetching first picture of post
#			f_url = urllib.urlopen(post_picture)
#			local_file = open('/tmp/' + file_hash + '.jpg', "w")
#			local_file.write(f_url.read())
#			local_file.close()
#		picture = "picture=" + post_picture
#		html = html + '<div><img src="' + 'file://' + '/tmp/' + file_hash + '.jpg"' + ' width="100" align="left"></div>'
