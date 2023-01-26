from .model import UserModel
from marshmallow import Schema, fields, ValidationError
from flask import jsonify
from src.core.api_errors import InputValidationError


class UserCreateDto(Schema):
    name = fields.String(required=True)
    last_name = fields.String(required=True)
    rut = fields.String(required=True)
    birthday = fields.DateTime(required=True)
    office = fields.String(required=True)


class UserUpdateDto(Schema):
    name = fields.String(dump_default=None)
    last_name = fields.String(dump_default=None)
    rut = fields.String(dump_default=None)
    birthday = fields.DateTime(dump_default=None)
    office = fields.String(dump_default=None)


class UserProjectReadDto(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    institution_id = fields.Integer()


class UserReadDto(Schema):
    # db info
    id = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    # properties
    name = fields.String()
    last_name = fields.String()
    rut = fields.String()
    birthday = fields.DateTime()
    office = fields.String()
    age = fields.Integer()

    # relations
    projects = fields.List(fields.Nested(UserProjectReadDto))


class UserMapper:
    def entity_to_summary(self, entity: UserModel):
        schema = UserReadDto(
            only=('id', 'name', 'last_name', 'age', 'office'))
        return schema.dump(entity)

    def entity_to_rut_view(self, entity: UserModel):
        schema = UserReadDto(
            only=('id', 'name', 'last_name', 'age', 'office', 'projects', 'rut'))
        return schema.dump(entity)

    def entity_to_details(self, entity: UserModel):
        schema = UserReadDto()
        return schema.dump(entity)

    def body_to_create_dto(self, body) -> UserCreateDto:
        schema = UserCreateDto()

        try:
            # Validate and transforms apply
            body = schema.load(body)
        except ValidationError as err:
            raise InputValidationError(err.messages)

        # set dump_default data and database-friendly format
        return schema.dump(body)

    def body_to_update_dto(self, body) -> UserUpdateDto:
        schema = UserUpdateDto()

        try:
            # Validate and transforms apply
            body = schema.load(body)
        except ValidationError as err:
            raise InputValidationError(err.messages)

        # set dump_default data and database-friendly format
        return schema.dump(body)
