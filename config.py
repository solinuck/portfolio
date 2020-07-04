import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "naweuiofösdfe"
    APP_PATH = dir_path
    IMAGE_UPLOADS = f"{dir_path}/portfolio_app/static/images/blog_uploads"
    DATABASE = f"{dir_path}/instance/flaskr.sqlite"
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]
    # MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024
    IMAGES_PATH = "http://localhost:5000/static/images"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    SECRET_KEY = "dev"

    IMAGE_UPLOADS = f"{dir_path}/portfolio_app/static/images/blog_uploads"


class TestingConfig(Config):
    TESTING = True
