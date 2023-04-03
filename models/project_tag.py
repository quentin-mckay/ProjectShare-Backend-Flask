from main import db

project_tag = db.Table(
    'project_tag',
	db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
)

# class ProjectTag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
    
#     project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
#     tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)
    
#     project = db.relationship('project', back_populates='tags')
#     tag = db.relationship('tag', back_populates='projects')