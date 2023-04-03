from flask import Blueprint, jsonify, request, abort
from main import db

from main import bcrypt

from models.users import User
from schemas.user_schema import user_schema

from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity



auth = Blueprint('auth', __name__, url_prefix='/auth')



@auth.route('/register', methods=['POST'])
def register():
    '''Create new user'''
    # load() converts from serialized format (JSON) to python dict 
    # AND also validates (makes sure data is in expected format and free of errors)
    user_fields = user_schema.load(request.json)
    
    # both of these are <class 'dict'>
    # print(type(request.json))
    # print(type(user_fields))
    
    username = user_fields.get('username')
    
    # Database query
    # Get the first User which has a username property equal to *username*
    user = User.query.filter_by(username=username).first() # returns None if didn't find anything
    
    if user:
        print('Username already exists. Aborting.')
        
        # CA example
        # return abort(400, description="username alread registered") # sends Content-Type: text/html
        
        return jsonify(message="That username already exists."), 409 # Conflict


    # Encyrpt password
    encrypted_password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    # Create and add new User to database
    new_user = User(
        username=user_fields['username'],
        password=encrypted_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Create new JWT
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(new_user.id), expires_delta=expiry)


    # can't just jsonify(new_user)
    # return user_schema.dump(new_user) # dump converts Python -> JSON (I don't need to wrap in jsonify())
    return jsonify(message="User registered successfully!", token=access_token, id=new_user.id), 201 # Created



@auth.route("/login", methods=['POST'])
def login():
    '''Log in a user using username and password'''
    # Extract POST data
    if request.is_json:
        user_fields = user_schema.load(request.json)
        # could then do ?
        # username, password = user_fields.values()
    else: # if it's a POST from a <form>
        user_fields = user_schema.load(request.form)
        
    
    username = user_fields.get('username')
    
    # Database query
    # Get the first User which has a username property equal to *username*
    user = User.query.filter_by(username=username).first()
    
    # Check if user exists
    if not user:
        return jsonify(message="You entered an invalid username"), 401 # Permission Denied
        # CA does
        # return abort(401, description="Incorrect username and password")
        
    # Check if sent password matches user password
    if not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return jsonify(message="You entered an invalid password"), 401 # Permission Denied
    
    # Create new JWT
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    
    
    return jsonify(message="Login succeeded!", token=access_token, id=user.id), 200


@auth.route('/token', methods=['POST'])
@jwt_required()
def authenticate_token():
    '''Check JWT is valid and return user id and name. Used for logging in automatically when the app first loads'''
    
    # Extract user id from JWT
    user_id = get_jwt_identity()

    # Database query
    # Get the User by it's primary key, the ID
    user = User.query.get(user_id)
    
    return jsonify(id=user_id, username=user.username), 200