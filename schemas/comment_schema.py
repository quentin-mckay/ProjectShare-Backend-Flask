from main import ma
from models.comments import Comment
from marshmallow import fields


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # ordered = True
        # Fields to expose. Card is not included as comments will be shown always attached to a Card.
        # fields = ("id", "message", "user")
        model = Comment
        
    user =  fields.Nested("UserSchema", only=("username",))  
      

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


# print('from comment schema')