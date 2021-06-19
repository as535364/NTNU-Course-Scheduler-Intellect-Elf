from app import db


class User(db.model):
    uid = db.Column(db.Integer, primary_key=True)
