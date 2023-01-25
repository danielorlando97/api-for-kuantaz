from .model import InstitutionModel
from marshmallow import Schema, fields, ValidationError
from src.core.api_errors import InputValidationError


class InstitutionCreateDto(Schema):
    name = fields.String(required=True)
    description = fields.String()
    direction = fields.String()


class InstitutionUpdateDto(Schema):
    name = fields.String(default=None)
    description = fields.String(default=None)
    direction = fields.String(default=None)


class InstitutionProjectUserReadDto(Schema):
    # db info
    id = fields.Integer()

    # properties
    name = fields.String()
    last_name = fields.String()
    rut = fields.String()
    office = fields.String()
    age = fields.Integer()


class InstitutionProjectReadDto(Schema):
    # db info
    id = fields.Integer()

    # properties
    name = fields.String()
    description = fields.String()
    start_date = fields.DateTime()
    end_date = fields.DateTime()

    main_user = fields.Nested(InstitutionProjectUserReadDto)


class InstitutionReadDto(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String(dump_default="It doesnt have description yet")
    direction = fields.String(dump_default="It doesnt have description yet")
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    projects = fields.List(fields.Nested(InstitutionProjectReadDto))


class InstitutionDirectionView(Schema):
    id = fields.Integer()
    direction = fields.Function(
        lambda obj: None if obj.direction is None else f'https://www.google.com/maps/search/{obj.direction}')
    name = fields.Function(lambda obj: obj.name[:3].upper())


class InstitutionMapper:
    def entity_to_summary(self, entity: InstitutionModel):
        schema = InstitutionReadDto(
            only=('id', 'name', 'description', 'direction'))
        return schema.dump(entity)

    def entity_to_direction_view(self, entity: InstitutionModel):
        schema = InstitutionDirectionView()
        return schema.dump(entity)

    def entity_to_details(self, entity: InstitutionModel):
        schema = InstitutionReadDto()
        return schema.dump(entity)

    def body_to_create_dto(self, body) -> InstitutionCreateDto:
        schema = InstitutionCreateDto()

        try:
            # Validate and transforms apply
            body = schema.load(body)
        except ValidationError as err:
            raise InputValidationError(err.messages)

        # set default data and database-friendly format
        return schema.dump(body)

    def body_to_update_dto(self, body) -> InstitutionUpdateDto:
        schema = InstitutionUpdateDto()

        try:
            # Validate and transforms apply
            body = schema.load(body)
        except ValidationError as err:
            raise InputValidationError(err.messages)

        # set default data and database-friendly format
        return schema.dump(body)
