from flask import Blueprint

from main import db
from main import bcrypt

from models.users import User
from models.projects import Project
from models.comments import Comment
from models.tags import Tag


db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_db():
	db.create_all()
	print("Tables created")
 
 

@db_commands.cli.command("seed")
def seed_db():
    seed()

def seed():
    #Create the users first
    # admin_user = User(
    #     email = "admin@email.com",
    #     # password = bcrypt.generate_password_hash("password123").decode("utf-8"),
    #     password = '1234',
    #     admin = True
    # )
    # db.session.add(admin_user)

    # password = bcrypt.generate_password_hash("123456").decode("utf-8")
    user1 = User(username = "Quentin", password = bcrypt.generate_password_hash("qwer").decode("utf-8"), admin = True)
    user2 = User(username = "Laura", password = bcrypt.generate_password_hash("asdf").decode("utf-8"))
    user3 = User(username = "Tino", password = bcrypt.generate_password_hash("zxcv").decode("utf-8"))
    
    db.session.add_all([user1, user2, user3])
    db.session.commit() # This extra commit will end the transaction and generate the ids for the user
    
    
    
    project1 = Project(
        title="Syntax Highlighter",
        description="Syntax highlighter for code blocks in the Ed platform",
        github_url="https://github.com/quentin-mckay/Code-Syntax-Highlighter-Ed",
        image_url="https://c.tadst.com/gfx/600x337/rainbow.jpg?1",
        user=user1
    ) # user field comes from User model backref
    project2 = Project(
        title="Text-to-Image Generator",
        description="Create images from text",
        github_url="https://github.com/quentin-mckay/OpenAI-Image-Generator-React-Frontend",
        demo_url="https://openai-image-generator-react-frontend.onrender.com/",
        image_url="https://www.wwf.org.uk/sites/default/files/styles/social_share_image/public/2022-05/_WW236934.jpg?itok=wsulCklO",
        user=user1
    )
    project3 = Project(
        title="Third project",
        description="Convert between binary, decimal, and hexidecimal bases using PyScript",
        github_url="https://github.com/quentin-mckay/Base-Converter-PyScript",
        image_url="https://pyscript.net/assets/images/pyscript-sticker-black.svg",
        user=user2
    )
    
    db.session.add_all([project1, project2, project3])
    db.session.commit()



    comment1 = Comment(message='Comment for the first project', user_id=2, project=project1) # project field from backref defined in Project model
    comment2 = Comment(message='Comment for the second project', user_id=3, project=project2)
    comment3 = Comment(message='Another comment for the second project', user_id=3, project=project2)
    comment4 = Comment(message='A comment for the third project', user_id=1, project_id=3) # another way to do it
    
    db.session.add_all([comment1, comment2, comment3, comment4])
    db.session.commit()


    tag1 = Tag(name='React')
    tag2 = Tag(name='Tailwind')
    tag3 = Tag(name='Flask')

    project1.tags.append(tag1)
    project1.tags.append(tag2)
    project2.tags.append(tag3)


    db.session.add_all([tag1, tag2, tag3])
    db.session.commit()


    




@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")
    
    
@db_commands.cli.command('reset')
def reset_db():
    
    db.drop_all()
    print("Tables dropped")
    
    db.create_all()
    print("Tables created")
    
    seed()
    print("Tables seeded")