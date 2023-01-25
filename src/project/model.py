
from src import db
from datetime import datetime


class ProjectModel(db.Model):
    __tablename__ = 'project'

    # db configs
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.now)

    # properties
    name = db.Column(db.String())
    description = db.Column(db.String())
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())

    # relations
    main_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    main_user = db.orm.relationship('UserModel', back_populates="projects")
    institution_id = db.Column(db.Integer, db.ForeignKey("institution.id"))
    institution = db.orm.relationship(
        'InstitutionModel', back_populates="projects")

    def __init__(self, name, description, start_date, end_date, main_user_id, institution_id):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.institution_id = institution_id
        self.main_user_id = main_user_id

    def __repr__(self):
        return f"Project<{self.name}>"
