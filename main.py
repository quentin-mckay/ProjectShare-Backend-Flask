from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()

def create_app():
    
    app = Flask(__name__)
    
    # still wouldn't allow post requests without preflight(?) stuff
    # cors.init_app(app, resources={r"/*": {"origins": "*", "methods": "*"}})
    
    # cors.init_app(app)
    CORS(app) # this worked too
    
    app.config.from_object('config.app_config')
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    
    from commands import db_commands
    app.register_blueprint(db_commands)


    # import the controllers and activate the blueprints
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    
    # @app.route('/')
    # def index():
    #     return 'hello world'
    
    return app