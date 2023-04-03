from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from main import db

from models.projects import Project
from models.comments import Comment

from schemas.comment_schema import comment_schema, comments_schema


comments = Blueprint("comments", __name__)

# GET /posts/:postId/comments - Retrieve a list of all comments for a specific post.
# GET /posts/:postId/comments/:id - Retrieve a specific comment for a specific post by ID.
# POST /posts/:postId/comments - Create a new comment for a specific post.
# PUT /posts/:postId/comments/:id - Update a specific comment for a specific post by ID.
# DELETE /posts/:postId/comments/:id - Delete a specific comment for a specific post by ID.

@comments.route('/projects/<int:project_id>/comments', methods=['GET'])
def get_single_project_comments(project_id: int):
    '''Get a project's comments'''
    
    # Database query
    # Get the first Project which has a id property equal to *project_id*
    project = Project.query.filter_by(id=project_id).first()
    
    return jsonify(comments_schema.dump(project.comments))


@comments.route('/projects/<int:project_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(project_id: int):
	user_id = get_jwt_identity()
	
	# Database query
    # Get the first Project which has a id property equal to *project_id*
	project = Project.query.filter_by(id=project_id).first() # or Project.query.get(project_id)
 
	# Check if project exists
	if not project:
		return jsonify(message="Project not found"), 404 # Not Found
  
	message = request.json.get('message')
 
	# Create comment and add to database
	comment = Comment(
     	message=message, 
		user_id=user_id,
		project=project
	)
 
	db.session.add(comment)
	db.session.commit()
 
	return jsonify(message="Comment added", comment=comment_schema.dump(comment))