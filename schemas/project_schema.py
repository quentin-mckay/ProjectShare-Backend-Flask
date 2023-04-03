from main import ma
from models.projects import Project
from marshmallow import fields


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        # exclude = ('user',) # this didn't real
        
    # this would be the other way
    # auto includes user_id in returned object
    # then do another axios call on the frontend to get the user info by user id
    # user_id = ma.auto_field() 
    
    # exclude nested projects in User to prevent circular dependency causing recursion overflow error
    # user = fields.Nested("UserSchema", exclude=("projects",)) 
    
    # or use only to pick out the fields I want
    user = fields.Nested("UserSchema", only=("username", "id")) 
    tags = fields.List(fields.Nested("TagSchema"))
    comments = fields.List(fields.Nested("CommentSchema"))
    
    
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


# print('from project schema')