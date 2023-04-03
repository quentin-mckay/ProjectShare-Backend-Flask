from main import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    
    # projects = db.relationship('ProjectTag', back_populates='tag')
    
    # project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    # card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    
    
    def __repr__(self):
        return f'<Tag {self.id} {self.title}>'