import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # setting a secret key to be used by flask to generate tokens by flask-WTF
    # The key can be generated by the os or use the hardcoded defined key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-key-is-totally-hard'
    # configure sqlalchemy with SQLlite, gets configuration from environment variable or falls back to hardcoded value
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False