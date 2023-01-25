from .model import ProjectModel
from marshmallow import Schema, fields, ValidationError, validates, validates_schema
from flask import jsonify
from src.core.api_errors import InputValidationError
from dateutil import relativedelta, parser
from datetime import datetime


class ProjectCreateDto(Schema):
    name = fields.String(required=True)
    description = fields.String(default='It doesnt have description yet')
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    main_user_id = fields.Integer(required=True)
    institution_id = fields.Integer(required=True)

    @validates_schema
    def validate_end_date(self, data, **kwargs):
        if data["start_date"] >= data["end_date"]:
            raise ValidationError(
                'The end date have to be a date after the start date')


class ProjectUpdateDto(Schema):
    name = fields.String(default=None)
    description = fields.String(default=None)
    start_date = fields.DateTime(default=None)
    end_date = fields.DateTime(default=None)
    main_user_id = fields.Integer(default=None)
    institution_id = fields.Integer(default=None)

    @validates_schema
    def validate_end_date(self, data, **kwargs):
        if "start_date" in data and "end_date" in data and data["start_date"] >= data["end_date"]:
            raise ValidationError(
                'The end date have to be a date after the start date')


class ProjectUserReadDto(Schema):
    # db info
    id = fields.Integer()

    # properties
    name = fields.String()
    last_name = fields.String()
    rut = fields.String()
    office = fields.String()
    age = fields.Integer()


class ProjectInstitutionReadDto(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    direction = fields.String()


class ProjectReadDto(Schema):
    # db info
    id = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    # properties
    name = fields.String()
    description = fields.String()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    days_to_release = fields.Function(lambda obj: relativedelta.relativedelta(
        datetime.now(), obj.end_date).days)
    # main_user_id = fields.Integer()

    # relation
    institution = fields.Nested(ProjectInstitutionReadDto)
    main_user = fields.Nested(ProjectUserReadDto)


class ProjectMapper:
    def entity_to_summary(self, entity: ProjectModel):
        schema = ProjectReadDto(
            only=('id', 'name', 'start_date', 'end_date'))
        return schema.dump(entity)

    def entity_to_details(self, entity: ProjectModel):
        schema = ProjectReadDto()
        return schema.dump(entity)

    def entity_to_durations(self, entity: ProjectModel):
        schema = ProjectReadDto(only=('id', 'name', 'days_to_release'))
        return schema.dump(entity)

        # delta = relativedelta.relativedelta(
        #     datetime.now(), parser.parse(entity.end_date))

        # result[''] = f'{delta.years}/{delta.months}/{delta.days}-{delta.hours}:{delta.minutes}'
        # return result

    def body_to_create_dto(self, body) -> ProjectCreateDto:
        schema = ProjectCreateDto()

        try:
            # Validate and transforms apply
            body = schema.load(body)
        except ValidationError as err:
            raise InputValidationError(err.messages)

        # set default data and database-friendly format
        return schema.dump(body)

    def body_to_update_dto(self, body) -> ProjectUpdateDto:
        schema = ProjectUpdateDto()

        try:
            # Validate and transforms apply
            body = schema.load(body)
        except ValidationError as err:
            raise InputValidationError(err.messages)

        # set default data and database-friendly format
        return schema.dump(body)
