from enum import unique
from . import db #from the current package import db object
from flask_login import UserMixin   #custom class for logging in 
from sqlalchemy.sql import func



#database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
    # A list like object that is created to store all the notes that will be created
    # Note is the exact name of the class 
    notes = db.relationship('Note')
    
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    #the user that created the note, the note should only be visible(queriable) to the person that made the note
    # user.id represents the id(primary_key) the user class in lower case
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
class Midi_file(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)