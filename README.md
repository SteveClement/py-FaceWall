
py-FaceWall
===========

Hello World

Dependencies
------------

* python
* [facebook-sdk](https://github.com/pythonforfacebook/facebook-sdk)
* python-ConfigParser
* python-urllib, python-urllib2


[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=SteveClement&url=https://github.com/SteveClement/py-FaceWall&title=Python FaceBook Wall and Printer&language=en_GB&tags=github&category=software) 

Release notes
=============

27.08.2012
----------

* added config file support. 
A config file must be named facebook.cfg and look like this:

	[facebook]
	app_id: myappid
	app_secret: mysupersecret
	
	[connection]
	proxy_host:
	proxy_port:
	
	[httpd]
	docroot:
