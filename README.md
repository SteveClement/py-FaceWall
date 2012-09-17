
py-FaceWall
===========

Hello World

Dependencies
------------

* python
* [facebook-sdk](https://github.com/pythonforfacebook/facebook-sdk)
* python-ConfigParser
* python-urllib, python-urllib2
* If Dymo Label Writer is used: wget http://global.dymo.com/img/compel/xKpID6d3hOi6UrMXDNF4k6IlSMSm3E_0.gz -O 
** CUPS-dev (libcups2-dev libcupsimage2-dev)
** build-essential
** cups


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
