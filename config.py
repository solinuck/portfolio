import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "naweuiofösdfe"
    APP_PATH = dir_path
    BLOG_UPLOADS = f"{dir_path}/portfolio_app/static/images/blog_uploads"
    PROJECT_UPLOADS = f"{dir_path}/portfolio_app/static/images/projects"
    DATABASE = f"{dir_path}/instance/flaskr.sqlite"
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]
    MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024
    IMAGES_PATH = "http://localhost:5000/static/images"
    IMAGE_UPLOADS_REL = "http://localhost:5000/static/images/blog_uploads"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    SECRET_KEY = "dev"

    BLOG_UPLOADS = f"{dir_path}/portfolio_app/static/images/blog_uploads"


class TestingConfig(Config):
    TESTING = True
