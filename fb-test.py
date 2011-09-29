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
	print '# The posters ID is: ' + unicode(poster_id)
	print '# This is post No: ' + unicode(rand_post) + ' data in post: ' + unicode(post)
	print '##########################################################################################################'
	print '-->'

# Generating HTML Headers
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
#feed = facebook_graph.get_connections("95283473324", "feed")

rand_post = random.randint(0, 24)
post = feed["data"][rand_post]

poster_name = unicode(post['from']['name'])
poster_id = post['from']['id']
poster_picture_url = 'http://graph.facebook.com/' + poster_id + '/picture?type=large'
profile_picture = "profile_picture=" + poster_picture_url

# Fetching Picture of poster
if os.path.exists('/usr/share/nginx/www/' + poster_id + '.jpg') == False:
	f_url = urllib.urlopen(poster_picture_url)
	local_file = open('/usr/share/nginx/www/' + poster_id + '.jpg', "w")
	local_file.write(f_url.read())
	local_file.close()
html = html + '  <div id="poster" class="norm"><img src="' + unicode(poster_id) + '.jpg" alt="Profile Picture of Poster"' + ' width="100" align="left">'
html = html + """    <br >
		"""
html = html + poster_name + ': '
##html = html + unicode(poster_name) + u' schréift: '
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
	html = html + """
"""

	post_likes = post.get('likes')
	if post_likes == None:
		#print 'No Likes yet :('
		likes = "0"
		html = html + '    <div id="likes" class="likes"><img src="thumbs-down.png" alt="Like Thumbs-up" height="100" align="top"><br >:(</div>'
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

##	html = html + '<div id="footer" class="norm">P.S: Bei Facebook bas de eng Nummer! An zwar: <b>' + unicode(poster_id) + '</b><br >'
##	html = html + """
##"""
##	html = html + '<br >Kee Plang wat di <b>Nummer</b> heescht??? Kee Problem komm bei de <img src="/tmp/header-logo.png" align="middle" height="17"> Stand a kuck der et selwer un.'
##	html = html + """
##</div>"""


	html = html + """
<br >
<br >
<br >
<br >
<br >
<br >
<br >
<br >
<br >
<!--
<p>
    <a href="http://validator.w3.org/check?uri=referer"><img
      src="http://www.w3.org/Icons/valid-html401" alt="Valid HTML 4.01 Transitional" height="31" width="88"></a>
</p>
<p>
    <a href="http://jigsaw.w3.org/css-validator/check/referer">
        <img style="border:0;width:88px;height:31px"
            src="http://jigsaw.w3.org/css-validator/images/vcss"
            alt="Valid CSS!" />
    </a>
</p>
-->
</body>
</html>
"""
	local_file = codecs.open('/usr/share/nginx/www/index.html', encoding='utf-8', mode="w")
	local_file.write(html)
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
