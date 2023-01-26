from flask_sqlalchemy import SQLAlchemy

from src.core.api_errors import ApplicationInconsistencyError
from .model import UserModel
from datetime import datetime
from dateutil import relativedelta, parser


class UserService:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def compute_age(self, birthday):

        date = parser.parse(birthday)

        delta = relativedelta.relativedelta(datetime.now(), date)
        return delta.years

    def create(self, data):
        new_user = UserModel(
            name=data["name"],
            last_name=data["last_name"],
            rut=data["rut"],
            birthday=data["birthday"],
            office=data["office"],
            age=self.compute_age(data["birthday"])
        )

        self.db.session.add(new_user)
        self.db.session.commit()

        return new_user

    def get_all(self):
        return UserModel.query.all()

    def get_by_id(self, _id) -> UserModel:
        entity = UserModel.query.get(_id)
        if entity is None:
            raise ApplicationInconsistencyError('institution not found')
        return entity

    def find_by_rut(self, rut):
        return UserModel.query.filter(UserModel.rut == rut)

    def update(self, _id, data):
        entity = self.get_by_id(_id)

        entity.name = entity.name if data["name"] is None else data["name"]
        entity.last_name = entity.last_name if data["last_name"] is None else data["last_name"]
        entity.rut = entity.rut if data["rut"] is None else data["rut"]
        entity.birthday = entity.birthday if data["birthday"] is None else data["birthday"]
        entity.office = entity.office if data["office"] is None else data["office"]
        entity.age = entity.age if data['birthday'] is None else self.compute_age(
            data["birthday"])

        self.db.session.add(entity)
        self.db.session.commit()

    def delete(self, _id):
        entity = self.get_by_id(_id)
        self.db.session.delete(entity)
        self.db.session.commit()
