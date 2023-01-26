from flask_sqlalchemy import SQLAlchemy
from .model import ProjectModel
from datetime import datetime
from src.core.api_errors import ApplicationInconsistencyError, ApplicationValidationError
from dateutil.parser import parser
from src.institution.service import InstitutionService
from src.user.service import UserService


class ProjectService:
    def __init__(self, db: SQLAlchemy, user_service: UserService, inst_service: InstitutionService) -> None:
        self.db = db
        self.user_service = user_service
        self.institution_service = inst_service

    def validate_user_selected(self, _id, default=None):
        if _id is None:
            return default

        return self.user_service.get_by_id(_id).id

    def validate_institution_selected(self, _id, default=None):
        if _id is None:
            return default

        return self.institution_service.get_by_id(_id).id

    def create(self, data):
        new_project = ProjectModel(
            name=data['name'],
            description=data['description'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            main_user_id=self.validate_user_selected(data['main_user_id']),
            institution_id=self.validate_institution_selected(
                data['institution_id'])
        )

        self.db.session.add(new_project)
        self.db.session.commit()

        return new_project

    def get_all(self):
        return ProjectModel.query.all()

    def get_by_id(self, _id) -> ProjectModel:
        entity = ProjectModel.query.get(_id)
        if entity is None:
            raise ApplicationInconsistencyError('project not found')
        return entity

    def update(self, _id, data):
        entity = self.get_by_id(_id)

        entity.name = entity.name if data['name'] is None else data['name']
        entity.description = entity.description if data['description'] is None else data['description']
        entity.start_date = entity.start_date if data['start_date'] is None else data['start_date']
        entity.main_user_id = self.validate_user_selected(
            data['main_user_id'], default=entity.main_user_id)

        entity.institution_id = self.validate_institution_selected(
            data['institution_id'], default=entity.institution_id)

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
