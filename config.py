import os

class DevelopmentConfig():
  SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  CACHE_TYPE = "SimpleCache"
  DEBUG = True