from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://student:student@localhost/food'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


conn = mysql.connector.connect(
    host='localhost', 
    database='food',
    user='student',
    password='student')

if conn.is_connected():
    print('Connected to database')
    cursor = conn.cursor(dictionary=True,buffered=True)
        #cursor.execute("SELECT * FROM course")
#engine = create_engine('mysql://student:student@localhost/food')
#connection = engine.raw_connection()
#cursor = connection.cursor()

from flaskDemo import routes
from flaskDemo import models

models.db.create_all()
