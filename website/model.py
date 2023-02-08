from .import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    fullname=db.Column(db.String(150))
    is_admin= db.Column(db.Boolean, default= False, nullable=False)
    
    

class Profileform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    amount = db.Column(db.Float)
    account = db.Column(db.Integer)
    receipt = db.Column(db.LargeBinary)
    qrcode = db.Column(db.LargeBinary)
    


