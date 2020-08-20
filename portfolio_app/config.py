import json

with open("/etc/portfolio_config.json") as config_file:
    config = json.load(config_file)


class Config(object):
    DEBUG = False
    TESTING = False
    GITHUB_TOKEN = config.get("GITHUB_TOKEN")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = config.get("SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True

    SECRET_KEY = "dev"
