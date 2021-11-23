from datetime import datetime
from flaskdemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

@login_manager.user_loader
def load_user(customer_id):
    return User.query.get(int(customer_id))


class User(db.Model, UserMixin):
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50), unique=True, nullable=False)
    customer_email = db.Column(db.String(80), unique=True, nullable=False)
    customer_address = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    customer_phone = db.Column(db.String(50))
    customer_type = db.Column(db.String(10), nullable=False)
    

    def __repr__(self):
        return f"User('{self.customer_name}', '{self.customer_email}')"

    def get_id(self):
           return (self.customer_id)
