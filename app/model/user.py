from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    dept_name = db.Column(db.String(80), default='')
    grade = db.Column(db.Integer, default=0)

    def __init__(self, email, username, password, is_admin=False, dept_name='', grade=0):
        self.email = email
        self.username = username
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.is_admin = is_admin
        self.dept_name = dept_name
        self.grade = grade
