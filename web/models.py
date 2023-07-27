from datetime import datetime
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    active = db.Column(db.Boolean())
    user_group = db.Column(db.String(100))
    created_on = db.Column(db.DateTime(), default=datetime.now())
    isadmin = db.Column(db.Boolean())
