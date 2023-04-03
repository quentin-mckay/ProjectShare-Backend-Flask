from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from main import db

from datetime import date

from models.users import User
from models.projects import Project
from models.tags import Tag
from schemas.project_schema import project_schema, projects_schema

import os
import cloudinary
import cloudinary.uploader


# Cloudinary setup
cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key = os.environ.get("CLOUDINARY_API_KEY"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
)


projects = Blueprint("projects", __name__, url_prefix="/projects")



@projects.route('/', methods=['GET'])
def get_all_projects():
    '''Get a list of all projects'''
    
    # Database query
    # Get all Projects
    project_list = Project.query.all()

    return jsonify(projects_schema.dump(project_list)), 200 # OK



@projects.route('/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id: int):
    '''Get a project by its ID'''
    
    # Database query
    # Get the Project by it's primary key, the ID
    project = Project.query.get(project_id) # shorthand for querying by primary_key
    # project = Project.query.filter_by(id=project_id).first() # alternative way
    
    # Check if project exists
    if not project:
        return jsonify(message="Project not found"), 404 # Not Found

    return jsonify(project_schema.dump(project)), 200 # OK



@projects.route('/', methods=['POST'])
@jwt_required() # planectary led to error without the parentheses
def create_project():
    '''Create a new project'''
    project_fields = request.json
    # project_fields = project_schema.load(request.json)
    
    # print(request.json)
    
    # extract id of user from the JWT token
    user_id = get_jwt_identity()
    
    
    title = project_fields.get('title')
    description = project_fields.get('description')
    github_url = project_fields.get('githubURL')
    demo_url = project_fields.get('demoURL')
    # image_url = project_fields.get('imageURL')
    image_url = ''
    
    # print('Tags: ', project_fields.get('tags'))
    tags = project_fields.get('tags')


    try:
        image = project_fields.get('image')
        
        # Upload image to Cloudinary
        if image:
            response = cloudinary.uploader.upload(image, folder='projectshare')
            # print('Image: yes')
            image_url = response.get('url')
        else:
            print('Image: no')


        # Create a new project
        new_project = Project(
            title=title,
            description=description,
            github_url=github_url,
            demo_url=demo_url,
            image_url=image_url,
            date=date.today(),
            user_id=user_id, # link the new project to the correct user,
            # tags=tags (this doesn't work. must do it manually like below)
        )
        
        # Add tags to the project
        for tag in tags:
            new_tag = Tag(name=tag)
            new_project.tags.append(new_tag)
        
        # Add project to the database
        db.session.add(new_project)
        db.session.commit()
        
        return jsonify(message="Project added", id=new_project.id), 201 # Created

    except Exception as e:
        return jsonify(message="Error while creating new Project"), 500 # Internal Server Error
    
    
    
@projects.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id: int):
    '''Update a project by its ID'''
    # project_fields = project_schema.load(request.json)
    project_fields = request.json
    # print(project_fields)

    user_id = get_jwt_identity()
    
    # CA examples
    # user = User.query.get(user_id)
    # if not user:
    #     return abort(401, message="Invalid user")


    # Database query
    # Get the Project by its primary key, the ID
    project = Project.query.get(project_id)
    
    
    # Check if project exits
    if not project:
        print('project not found')
        return jsonify(message="Project not found"), 404 # Not Found
    
    # Check if used ID from JWT matches project's user ID
    if int(user_id) != project.user.id:
        print('ids dont match')
        return jsonify(message="Unauthorized user"), 401 # Unauthorized (abort send backs html)
    
    try:
        # Create project and add 
        project.title = project_fields.get('title')
        project.description = project_fields.get('description')
        project.github_url = project_fields.get('githubURL')
        project.demo_url = project_fields.get('demoURL')
        # project.image_url = project_fields.get('imageURL')
    
        # replace tag list
        project.tags = [Tag(name=name) for name in project_fields.get('tags')]
        
        db.session.commit()
        
        return jsonify(message="Updated project", project=project_schema.dump(project)), 202 # Accepted
    except:
        return jsonify(message="Error while creating new Project"), 500 # Internal Server Error



@projects.route('/<int:project_id>', methods=['POST'])
@jwt_required()
def delete_project(project_id: int):
    '''Delete a project by its ID'''
    user_id = get_jwt_identity()
    # user_id = 2
    
    # Database query
    # Get the User by its primary key, the ID
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="Invalid user"), 401
    
    
    # Database query
    # Get the Project by its primary key, the ID
    project = Project.query.get(project_id)
    
    # print('project username and id:', project.user.username, project.user_id)
    # print('user id:', user_id)
    # print('project_id:', project_id)
    # print('project.user.id', project.user.id)
    
    # Check the project exists
    if not project:
        return jsonify(message="Project does not exist"), 404 # Not Found
    
    # Check if used ID from JWT matches project's user ID
    if int(user_id) != project.user.id:
        print('here')
        return jsonify(message="Unauthorized user"), 401 # Unauthorized (abort send backs html)
    
    # Delete the project
    db.session.delete(project)
    db.session.commit()
    
    return jsonify(message="Project deleted", id=project_id), 202 # Accepted



@projects.route('/tag', methods=['GET'])
def get_projects_by_tag_name():
    '''Get all projects that contain a specific tag in their tags list'''
    tag_name = request.args.get('tag')

    # projects = Project.query.filter(Project.tags.any(tag_name)).all() (not working)
    
    # Database query
    # Join the Project model with the Tag model via the project_tags table.
    # The project_tags table is passed to the *secondary* parameter of the relationship method in the Project model
    # Then select all projects that have a tags field that includes *tag_name* 
    projects = Project.query.join(Project.tags).filter(Tag.name == tag_name).all()
    
    return jsonify(projects_schema.dump(projects))