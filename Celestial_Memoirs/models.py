from Celestial_Memoirs import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable = False,unique=True)
    email = db.Column(db.String(120),nullable = False,unique=True)
    password = db.Column(db.String(60),nullable=False)
    entries = db.relationship('Entries',backref='author',lazy=True)
    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}')"

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    def __repr__(self):
        return f"Post('{self.date}','{self.content}')"
  