# -*- coding:utf8 -*-
import os
import json


class ReadConfigJson(object):

    def __init__(self):
        path = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(path, 'config.json')
        self.config_path = config_path

    def __read_json(self):
        with open(self.config_path, encoding='utf-8') as f:
            data = f.read()
            data = json.loads(data)
        return data

    def get_mysql_config(self):
        mysql_dict = self.__read_json()['mysql']
        mysql_url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(user=mysql_dict['user'],
                                                                                        password=mysql_dict['password'],
                                                                                        host=mysql_dict['host'],
                                                                                        port=mysql_dict['port'],
                                                                                        database=mysql_dict['database'])

        return mysql_url


def read_sqlite_url():
    path = os.path.abspath(os.path.dirname(__file__))
    sqlit_path = os.path.join(path, 'db', 'data.db')

    return 'sqlite:///%s' % sqlit_path


base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
conf_path = os.path.join(base_path, 'console', 'config')
app_path = os.path.join(base_path, 'console', 'app_config', 'process.json')

upload_base_path = os.path.join(base_path, 'upload')
upload_doc_path = os.path.join(base_path, 'upload', 'doc')
upload_video_path = os.path.join(base_path, 'upload', 'video')



class Config:
    DEBUG = True
    # SECRET_KEY = os.urandom(24)
    SECRET_KEY = 'fm'

    SQLALCHEMY_DATABASE_URI = ReadConfigJson().get_mysql_config()
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    BOOTSTRAP_SERVE_LOCAL = True
    FLASKY_PER_PAGE = 20

    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

    ASSETS_DEBUG = False

    CONFIG_PATH = conf_path
    APP_CONFIG_PATH = app_path

    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '951995314@qq.com'
    MAIL_PASSWORD = 'ktlwclelryfdbcae'
    MAIL_DEFAULT_SENDER = '951995314@qq.com'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <951995314@qq.com>'
    FLASKY_ADMIN = None

    UPLOAD_DOC_DIR = upload_doc_path
    UPLOADS_DEFAULT_DEST = upload_video_path

    @staticmethod
    def init_app(app):
        pass
