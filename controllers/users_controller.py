from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from main import db

from models.users import User
from schemas.user_schema import user_schema, users_schema
from schemas.project_schema import project_schema, projects_schema

from schemas.tag_schema import tag_schema
from schemas.comment_schema import comment_schema

users = Blueprint("users", __name__, url_prefix="/users")


@users.get("/")
def get_users():
    '''Get a list of all users'''
    
    # Database query
    # Get all Users
    users_list = User.query.all()
    
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify(users_schema.dump(users_list))


@users.get('/<int:id>')
def get_user(id: int):
    '''Get a single user by ID'''
    
    # Database query
    # Get the User by its primary key, the ID
    user = User.query.filter_by(id=id).first() # User.get(id) did not work (flask-marshmallow docs are wrong)

    return user_schema.dump(user)


@users.get('/<int:id>/projects')
def get_user_projects(id: int):
    '''Get a list of projects'''
    
    # Database query
    # Get the User by its primary key, the ID
    user = User.query.filter_by(id=id).first() # or User.query.get(id)
    
    return projects_schema.dump(user.projects)