from src.institution.model import InstitutionModel
import pytest
from src.institution.dtos_mapper import InstitutionMapper
from src.core.api_errors import InputValidationError


from datetime import datetime

name = 'Tomas'
last_name = "Alasdos"
rut = '123456789'
birthday = datetime.now()
office = 'developer'


# @pytest.fixture(scope='module')
# def new_mapper():
#     return InstitutionMapper()


# def test_create_model(new_institution: InstitutionModel):
#     assert new_institution.name == name
#     assert new_institution.description == description
#     assert new_institution.direction == direction


# def test_map_summary(new_institution: InstitutionModel, new_mapper: InstitutionMapper):
#     dto = new_mapper.entity_to_summary(new_institution)

#     assert new_institution.name == dto['name']
#     assert new_institution.description == dto['description']
#     assert new_institution.direction == dto['direction']
#     assert len(dto) == 4


# def test_map_direction_view(new_institution: InstitutionModel, new_mapper: InstitutionMapper):
#     dto = new_mapper.entity_to_direction_view(new_institution)

#     assert new_institution.name[:3].upper() == dto['name']
#     assert f'https://www.google.com/maps/search/{new_institution.direction}' == dto['direction']
#     assert len(dto) == 3


# def test_entity_to_details(new_institution: InstitutionModel, new_mapper: InstitutionMapper):
#     dto = new_mapper.entity_to_details(new_institution)

#     assert new_institution.name == dto['name']
#     assert new_institution.description == dto['description']
#     assert new_institution.direction == dto['direction']
#     assert not dto['created_at'] is None

#     assert type(dto['projects']) == list


# def test_create_validate_success_maximal_data(new_mapper: InstitutionMapper):
#     try:
#         data = new_mapper.body_to_create_dto({
#             'name': name,
#             'description': description,
#             'direction': direction
#         })

#         assert data['name'] == name
#         assert data['description'] == description
#         assert data['direction'] == direction
#     except InputValidationError:
#         assert False


# def test_create_validate_success_minimal_data(new_mapper: InstitutionMapper):
#     try:
#         data = new_mapper.body_to_create_dto({
#             'name': name
#         })

#         assert data['name'] == name
#         assert data['description'] == None
#         assert data['direction'] == None
#     except InputValidationError:
#         assert False


# def test_create_validate_fail_by_name_missing(new_mapper: InstitutionMapper):
#     try:
#         new_mapper.body_to_create_dto({
#             'description': ''
#         })

#         assert False

#     except InputValidationError:
#         pass


# def test_create_validate_fail_by_error_field(new_mapper: InstitutionMapper):
#     try:
#         new_mapper.body_to_create_dto({
#             'description2': ''
#         })
#         assert False
#     except InputValidationError:
#         pass


# def test_update_validate_success_maximal_data(new_mapper: InstitutionMapper):
#     try:
#         data = new_mapper.body_to_update_dto({
#             'name': name,
#             'description': description,
#             'direction': direction
#         })

#         assert data['name'] == name
#         assert data['description'] == description
#         assert data['direction'] == direction
#     except InputValidationError:
#         assert False


# def test_update_validate_success_minimal_data(new_mapper: InstitutionMapper):
#     try:
#         data = new_mapper.body_to_update_dto({
#         })

#         assert data['name'] == None
#         assert data['description'] == None
#         assert data['direction'] == None
#     except InputValidationError:
#         assert False


# def test_update_validate_fail_by_error_field(new_mapper: InstitutionMapper):
#     try:
#         new_mapper.body_to_update_dto({
#             'description2': ''
#         })
#         assert False
#     except InputValidationError:
#         pass
