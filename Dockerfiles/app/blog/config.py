import os

class Config(object):


	SECRET_KEY = os.getenv('SECRET_KEY') or '123'
	DEBUG = True
	
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'work.db')
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

	DEBUG_TB_INTERCEPT_REDIRECTS = False
	DEBUG_TB_PROFILER_ENABLED = 'user-enabled'

	CACHE_TYPE = 'simple'
	CACHE_DEFAULT_TIMEOUT = 300


	SEND_LOGS = False
	INFO_LOG = "info.log"
	ERROR_LOG = "error.log"

	UPLOAD_FOLDER = '/home/pi/www/web/blog/tmp/'
	ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

	POSTS_PER_PAGE = 10
	#DEBUG_TB_ENABLED = False


	QINIU_ACCESS_KEY = '8S6pCI7xgpcW4b8p0ACDTyt3ZhYbMqqtO3fJFeYw'
	QINIU_SECRET_KEY = '8Ff-6WRb7kqdwEgKaFOxl81WXDDSJcmVJnexoJgX'
	PIC_BUCKET = 'yalove'
	PIC_DOMAIN = ''
	
class Testing(Config):
	pass
		

class ProductionConfig(Config):
	MYSQL_USER = os.getenv('MYSQL_USER') or 'aliyunyalove'
	MYSQL_PASS = os.getenv('MYSQL_PASS') or 'aliyunyalove123'
	MYSQL_HOST = os.getenv('MYSQL_HOST') or 'localhost'
	MYSQL_PORT = os.getenv('MYSQL_PORT') or '3306'
	MYSQL_DB = os.getenv('MYSQL_DB') or 'blog'
	SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (
        MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB
    )
	PREFERRED_URL_SCHEME = 'https'


config = {
	'default' : Testing,
	'produce' : ProductionConfig,
}
		