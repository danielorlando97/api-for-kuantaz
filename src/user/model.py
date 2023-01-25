
from src import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'user'

    # db configs
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.now)

    # properties
    name = db.Column(db.String())
    last_name = db.Column(db.String())
    rut = db.Column(db.String())
    birthday = db.Column(db.DateTime)
    office = db.Column(db.String())
    age = db.Column(db.Integer)

    # relations
    projects = db.orm.relationship(
        'ProjectModel', back_populates="main_user")

    def __init__(self, name, last_name, rut, birthday, office, age):
        self.name = name
        self.last_name = last_name
        self.rut = rut
        self.birthday = birthday
        self.office = office
        self.age = age

    def __repr__(self):
        return f"User<{self.name}>"
