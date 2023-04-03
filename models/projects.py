from main import db
from .project_tag import project_tag


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    github_url = db.Column(db.String, nullable=False)
    demo_url = db.Column(db.String)
    image_url = db.Column(db.String)
    date = db.Column(db.Date())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)        # a project is a child of User

    comments = db.relationship('Comment', backref='project', cascade='all, delete')  # first half of one-to-many relationship
    
    tags = db.relationship('Tag', secondary=project_tag, backref='projects')         # hook up to join table 
    
    
    # tags = db.relationship('ProjectTag', back_populates='project')

    # comments = db.relationship(
    #     "Comment",
    #     backref="card",
    #     cascade="all, delete"
    # )

    def __repr__(self):
        # project_content = self.content[:10] + '...'
        return f'<Project {self.id} {self.title}>'
