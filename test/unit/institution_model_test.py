from src.institution.model import InstitutionModel
import pytest
from src.institution.dtos_mapper import InstitutionMapper
from src.core.api_errors import InputValidationError

import tools.institutions as inst_helper


@pytest.fixture(scope='module')
def new_mapper():
    return InstitutionMapper()

#
#   MODEL TEST
#


def test_create_model():
    new_institution = inst_helper.create()

    assert new_institution.name == inst_helper.name
    assert new_institution.description == inst_helper.description
    assert new_institution.direction == inst_helper.direction


#
#   VIEW TEST
#


def test_map_summary(new_mapper: InstitutionMapper):
    new_institution = inst_helper.create()

    dto = new_mapper.entity_to_summary(new_institution)

    assert new_institution.name == dto['name']
    assert new_institution.description == dto['description']
    assert new_institution.direction == dto['direction']
    assert len(dto) == 4


def test_map_direction_view(new_mapper: InstitutionMapper):
    new_institution = inst_helper.create()

    dto = new_mapper.entity_to_direction_view(new_institution)

    assert new_institution.name[:3].upper() == dto['name']
    assert f'https://www.google.com/maps/search/{new_institution.direction}' == dto['direction']
    assert len(dto) == 3


def test_entity_to_details(new_mapper: InstitutionMapper):
    new_institution = inst_helper.create()

    dto = new_mapper.entity_to_details(new_institution)

    assert new_institution.name == dto['name']
    assert new_institution.description == dto['description']
    assert new_institution.direction == dto['direction']
    assert 'created_at' in dto
    assert 'updated_at' in dto

    assert type(dto['projects']) == list


#
#   VALIDATION TEST
#


def test_create_validate_success_maximal_data(new_mapper: InstitutionMapper):
    try:
        data = new_mapper.body_to_create_dto({
            'name': inst_helper.name,
            'description': inst_helper.description,
            'direction': inst_helper.direction
        })

        assert data['name'] == inst_helper.name
        assert data['description'] == inst_helper.description
        assert data['direction'] == inst_helper.direction
    except InputValidationError:
        assert False


def test_create_validate_success_minimal_data(new_mapper: InstitutionMapper):
    try:
        data = new_mapper.body_to_create_dto({
            'name': inst_helper.name
        })

        assert data['name'] == inst_helper.name
        assert data['description'] == None
        assert data['direction'] == None
    except InputValidationError:
        assert False


def test_create_validate_fail_by_name_missing(new_mapper: InstitutionMapper):
    try:
        new_mapper.body_to_create_dto({
            'description': ''
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_error_field(new_mapper: InstitutionMapper):
    try:
        new_mapper.body_to_create_dto({
            'description2': ''
        })
        assert False
    except InputValidationError:
        pass


def test_update_validate_success_maximal_data(new_mapper: InstitutionMapper):
    try:
        data = new_mapper.body_to_update_dto({
            'name': inst_helper.name,
            'description': inst_helper.description,
            'direction': inst_helper.direction
        })

        assert data['name'] == inst_helper.name
        assert data['description'] == inst_helper.description
        assert data['direction'] == inst_helper.direction
    except InputValidationError:
        assert False


def test_update_validate_success_minimal_data(new_mapper: InstitutionMapper):
    try:
        data = new_mapper.body_to_update_dto({
        })

        assert data['name'] == None
        assert data['description'] == None
        assert data['direction'] == None
    except InputValidationError:
        assert False


def test_update_validate_fail_by_error_field(new_mapper: InstitutionMapper):
    try:
        new_mapper.body_to_update_dto({
            'description2': ''
        })
        assert False
    except InputValidationError:
        pass
