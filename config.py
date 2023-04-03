import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # access to .env and get the value of SECRET_KEY,
    # the variable name can be any but needs to match
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")

    JSON_SORT_KEYS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # access to .env and get the value of DATABASE_URL,
        # the variable name can be any but needs to match
        value = os.environ.get("DATABASE_URI")

        if not value:
            raise ValueError("DATABASE_URI is not set")

        return value


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True


environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
