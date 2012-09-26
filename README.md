
py-FaceWall
===========

Hello World

Dependencies
------------

* python
* [facebook-sdk](https://github.com/pythonforfacebook/facebook-sdk)
* python-ConfigParser
* python-urllib, python-urllib2
* for twitter support: 
	** https://github.com/bear/python-twitter (OR maybe not)
	** oauth2
	** setuptools egg (all bundled)

* nginx
* If Dymo Label Writer is used: wget http://global.dymo.com/img/compel/xKpID6d3hOi6UrMXDNF4k6IlSMSm3E_0.gz -O dymo-cups-drivers-1.2.0.tar.gz OR wget http://www.dymo.com/media/Software/dymo-cups-drivers-1.2.0.tar.gz
** CUPS-dev (libcups2-dev libcupsimage2-dev)
** build-essential
** cups
/!\ Make sure you apply the pach for the driver to avoid compile errors

Installation
------------

Install & launch nginx (apt-get install nginx)

Set permissions:

$ sudo usermod -a -G www-data $USER
$ sudo chmod 770 /usr/share/nginx/www
$ sudo chgrp www-data /usr/share/nginx/www
$ sudo cp css/main.css /usr/share/nginx/www/
$ sudo cp images/* /usr/share/nginx/www/

Edit facebook.cfg 

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
	feed_id: numeric_feed_id

	[twitter]
	enable: true

	[connection]
	proxy_host:
	proxy_port:
	
	[httpd]
	docroot: /usr/share/nginx/www
