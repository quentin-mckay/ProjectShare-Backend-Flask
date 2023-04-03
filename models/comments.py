from main import db

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    message = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id} {self.message}>'