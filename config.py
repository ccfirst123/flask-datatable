import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = 'Your Secret Key, make it more complicated'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    @staticmethod
    def init_app(app):
        pass
