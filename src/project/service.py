from flask_sqlalchemy import SQLAlchemy
from .model import ProjectModel
from datetime import datetime
from src.core.api_errors import ApplicationValidationError
from dateutil.parser import parser


class ProjectService:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def create(self, data):
        new_project = ProjectModel(
            name=data['name'],
            description=data['description'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            main_user_id=data['main_user_id'],
            institution_id=data['institution_id']
        )

        self.db.session.add(new_project)
        self.db.session.commit()

        return new_project

    def get_all(self):
        return ProjectModel.query.all()

    def get_by_id(self, _id) -> ProjectModel:
        return ProjectModel.query.get_or_404(_id)

    def update(self, _id, data):
        entity = self.get_by_id(_id)

        entity.name = entity.name if data['name'] is None else data['name']
        entity.description = entity.description if data['description'] is None else data['description']
        entity.start_date = entity.start_date if data['start_date'] is None else data['start_date']
        entity.main_user_id = entity.main_user_id if data[
            'main_user_id'] is None else data['main_user_id']
        entity.institution_id = entity.institution_id if data[
            'institution_id'] is None else data['institution_id']

        if not data['end_date'] is None:
            if data['start_date'] is None:
                end = parser(data['end_date'])

                if entity.start_date >= end:
                    raise ApplicationValidationError(
                        'The end date have to be a date after the start date')

            entity.end_date = data['end_date']

        self.db.session.add(entity)
        self.db.session.commit()

    def delete(self, _id):
        entity = self.get_by_id(_id)
        self.db.session.delete(entity)
        self.db.session.commit()
