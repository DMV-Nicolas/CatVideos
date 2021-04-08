import os

DBDIR=f"sqlite:///{os.path.abspath(os.getcwd())}/database.db"
DB_URI="mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="",
    password="",
    hostname="",
    databasename=""
)
class Config(object):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_POOL_RECYCLE=250

class ProductionConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=DB_URI
    SECRET_KEY="123456789"#os.environ["SECRET_KEY"]

class DevelopmentConfig(Config):
    DEBUG=True
    SECRET_KEY="SSP-12J+Puihsaydugj7aSDTBUYASd"
    SQLALCHEMY_DATABASE_URI=DBDIR
#https://www.youtube.com/watch?v=ZzuaVv7SEiw
