
from src import db
from datetime import datetime


class InstitutionModel(db.Model):
    __tablename__ = 'institution'

    # db configs
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.now)

    # properties
    name = db.Column(db.String())
    description = db.Column(db.String())
    direction = db.Column(db.String())

    # relations
    projects = db.orm.relationship(
        'ProjectModel', back_populates="institution")

    def __init__(self, name, description, direction):
        self.name = name
        self.description = description
        self.direction = direction

    def __repr__(self):
        return f"Institution<{self.name}>"
