import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    APP_PATH = os.path.dirname(os.path.realpath(__file__))
    BLOG_UPLOADS = f"{APP_PATH}/portfolio_app/static/images/blog_uploads"
    PROJECT_UPLOADS = f"{APP_PATH}/portfolio_app/static/images/projects"
    IMAGES_PATH = "http://localhost:5000/static/images"
    IMAGE_UPLOADS_REL = "http://localhost:5000/static/images/blog_uploads"
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    APP_PATH = os.path.dirname(os.path.realpath(__file__))

    SECRET_KEY = "dev"

    BLOG_UPLOADS = f"{APP_PATH}/portfolio_app/static/images/blog_uploads"


class TestingConfig(Config):
    TESTING = True
