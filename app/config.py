#configuration for the lidar backend

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'development_key'
	WTF_CSRF_SECRET_KEY="a csrf secret key"
