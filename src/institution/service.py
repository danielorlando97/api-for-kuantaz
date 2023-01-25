from flask_sqlalchemy import SQLAlchemy
from .model import InstitutionModel
from datetime import datetime


class InstitutionService:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def create(self, data):
        new_institution = InstitutionModel(
            name=data['name'],
            description=data['description'],
            direction=data['direction']
        )

        self.db.session.add(new_institution)
        self.db.session.commit()

        return new_institution

    def get_all(self):
        return InstitutionModel.query.all()

    def get_by_id(self, _id) -> InstitutionModel:
        return InstitutionModel.query.get_or_404(_id)

    def update(self, _id, data):
        entity = self.get_by_id(_id)
        entity.name = entity.name if data['name'] is None else data['name']
        entity.description = entity.description if data['description'] is None else data['description']
        entity.direction = entity.direction if data['direction'] is None else data['direction']

        self.db.session.add(entity)
        self.db.session.commit()

    def delete(self, _id):
        entity = self.get_by_id(_id)
        self.db.session.delete(entity)
        self.db.session.commit()
