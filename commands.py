from flask import Blueprint

from datetime import date

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
    
    
    
    project_syntax = Project(
        title="Syntax Highlighter Chrome Extension",
        description="Syntax highlighter for code blocks in the Ed platform.",
        github_url="https://github.com/quentin-mckay/Code-Syntax-Highlighter-Ed",
        demo_url="https://chrome.google.com/webstore/detail/code-syntax-highlighter-f/cmbplgilmheonekccfhdoljbaenlkhff",
        image_url="https://github.com/quentin-mckay/Code-Syntax-Highlighter-Ed/blob/master/images/512.png?raw=true",
        
        user=user1
    ) # user field comes from User model backref
    project_textimage = Project(
        title="Text-to-Image Generator",
        description="Create images from text using OpenAI's DALL-E api using React and Flask.",
        github_url="https://github.com/quentin-mckay/OpenAI-Image-Generator-React-Flask",
        demo_url="https://openai-image-generator-react-frontend.onrender.com/",
        image_url="https://res.cloudinary.com/dnd7nhycm/image/upload/v1680230736/dalle3_icqy36.png",
        user=user2
    )
    project_converter = Project(
        title="Base Converter",
        description="Convert between binary, decimal, and hexidecimal bases using PyScript in the browswer.",
        github_url="https://github.com/quentin-mckay/Base-Converter-PyScript",
        demo_url="https://base-converter-pyscript.onrender.com/",
        image_url="https://github.com/quentin-mckay/Base-Converter-PyScript/raw/master/images/app-screenshot.jpg",
        user=user2
    )
    project_pendulum = Project(
        title="Pendulum Wave",
        description="Pendulum wave audio-visualization with MIDI out",
        github_url="https://github.com/quentin-mckay/Pendulum-Wave",
        demo_url="https://pendulum-wave.netlify.app/",
        image_url="https://github.com/quentin-mckay/Pendulum-Wave/raw/main/img/screenshot.jpg",
        date=date.today(),
        user=user1
    )
    
    db.session.add_all([
        project_syntax, 
        project_textimage, 
        project_converter, 
        project_pendulum
    ])

    db.session.commit()


    # COMMENTS
    comment1 = Comment(message='Comment for the first project', user_id=2, project=project_syntax) # project field from backref defined in Project model
    comment2 = Comment(message='Comment for the second project', user_id=3, project=project_textimage)
    comment3 = Comment(message='Another comment for the second project', user_id=1, project=project_textimage)
    comment4 = Comment(message='A comment for the third project', user_id=1, project_id=3) # another way to do it
    
    db.session.add_all([comment1, comment2, comment3, comment4])
    db.session.commit()


    # TAGS
    tag_react = Tag(name='React')
    tag_tailwind = Tag(name='Tailwind')
    tag_flask = Tag(name='Flask')
    tag_python = Tag(name='Python')
    tag_javascript = Tag(name='JavaScript')
    tag_webaudio = Tag(name="WebAudio")
    tag_webmidi = Tag(name="WebMIDI")
    tag_p5 = Tag(name="p5.js")

    project_syntax.tags.append(tag_javascript)
    
    project_textimage.tags.append(tag_react)
    project_textimage.tags.append(tag_tailwind)
    project_textimage.tags.append(tag_flask)

    project_converter.tags.append(tag_python)
    
    project_pendulum.tags.append(tag_javascript)
    project_pendulum.tags.append(tag_webaudio)
    project_pendulum.tags.append(tag_p5)
    project_pendulum.tags.append(tag_webmidi)

    db.session.add_all([tag_react, tag_tailwind, tag_flask])
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