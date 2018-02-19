import os
from flask_uploads import IMAGES

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in \
                   ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('发件邮箱')
    MAIL_PASSWORD = os.environ.get('邮箱密码')
    FLASKY_MAIL_SUBJECT_PREFIX = os.environ.get('主题前缀', '新用户')
    FLASKY_MAIL_SENDER = os.environ.get('发件邮箱')
    FLASKY_ADMIN = os.environ.get('收件邮箱')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    UPLOADED_PHOTO_DEST = 'H:/flasky/learning/flasky/DATA/Head_portrait'
    # UPLOADED_PHOTO_DEST = '/app/uploads'
    UPLOADED_PHOTO_ALLOW = IMAGES

    FLASKY_POSTS_PER_PAGE = 20

    # MAX_CONTENT_LENGTH = 1.1 * 1024 * 1024
    # UPLOADED_PHOTO_URL = 'http://127.0.0.1:5000/'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://root:and370sql@localhost:3306/FLASK_2?charset=utf8'


'''

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

'''
config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,

    'default': DevelopmentConfig
}
