import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "IkH1wokuYzqLE2c-J9XUmEGUF-q2k1DssOYl02RyFe4")
    DEBUG = False
    APP_NAME = 'LOL Champions'
    APP_SHORTNAME = 'LOL-C'

    # Flask jsonify settings
    JSONIFY_MIMETYPE = "application/json"


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    DB_PORT = os.getenv('DB_PORT', default=3306)
    DB_USER = os.getenv('DB_USER', default='root')
    DB_HOST = os.getenv('DB_HOST', default='localhost')
    DB_NAME = os.getenv('DB_NAME', default='lolchampions')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI =  f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass

if os.getenv('CONFIG') == 'dev':
    config = DevelopmentConfig
elif os.getenv('CONFIG') == 'prod':
    config = ProductionConfig
else:
    raise
