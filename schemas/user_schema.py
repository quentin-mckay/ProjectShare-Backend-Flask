from main import ma
from models.users import User
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        
    # use this to include project in each user (probably bad practice)
    # projects = fields.List(fields.Nested("ProjectSchema"), exclude=("user",))
        

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# print('from user schema')