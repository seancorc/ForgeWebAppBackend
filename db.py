from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.completed = kwargs.get(bool('completed'), False)

    def serialize(self):
        
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }


