import os

from dotenv import load_dotenv, dotenv_values
load_dotenv()

print(dotenv_values())

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # access to .env and get the value of SECRET_KEY,
    # the variable name can be any but needs to match
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")

    JSON_SORT_KEYS = False

    


class DevelopmentConfig(Config):
    DEBUG = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # access to .env and get the value of DATABASE_URL,
        # the variable name can be any but needs to match
        value = os.environ.get("DATABASE_URI")
        
        print(f"Database: {value}")

        if not value:
            raise ValueError("DATABASE_URI is not set")

        return value

class ProductionConfig(Config):
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        
        value = os.environ.get("RENDER_DATABASE_URI") # from external
        
        print(f"Database: {value}")

        if not value:
            raise ValueError("RENDER_DATABASE_URI is not set") # from external

        return value


class TestingConfig(Config):
    TESTING = True


class DeployConfig(Config):
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        
        value = os.environ.get("RENDER_INTERNAL_DATABASE_URI")
        
        print(f"Render Internal Database: {value}")

        if not value:
            raise ValueError("RENDER_INTERNAL_DATABASE_URI is not set")

        return value


# seems to come from .flaskenv only on local
# but 
environment = os.environ.get("FLASK_ENV") 

print(f"Environment: {environment}")

if environment == "production":
    app_config = ProductionConfig()
    print('Production Config Loaded')
elif environment == "deploy":
    app_config = DeployConfig()
    print('Deployment Config Loaded')
else:
    app_config = DevelopmentConfig()
    print('Development Config Loaded')




# @property
    # def SQLALCHEMY_DATABASE_URI(self):
    #     # access to .env and get the value of DATABASE_URL,
    #     # the variable name can be any but needs to match
    #     value = os.environ.get("DATABASE_URI")

    #     if not value:
    #         raise ValueError("DATABASE_URI is not set")

    #     return value