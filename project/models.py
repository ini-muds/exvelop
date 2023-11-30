from flask_login import UserMixin
from datetime import datetime
import pytz
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    image_url = db.Column(db.String(200), nullable=True)
    code = db.Column(db.String(1000), nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    