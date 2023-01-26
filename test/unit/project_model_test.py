from src.project.model import ProjectModel
import pytest
from src.project.dtos_mapper import ProjectMapper
from src.core.api_errors import InputValidationError
from dateutil import relativedelta, parser
import tools.project as project_helper


@pytest.fixture(scope='module')
def new_mapper():
    return ProjectMapper()

#
#   MODEL TEST
#


def test_create_model():
    new_project = project_helper.create(1, 2)

    assert new_project.name == project_helper.name
    assert new_project.description == project_helper.description
    assert new_project.main_user_id == 1
    assert new_project.institution_id == 2

#
#   VIEW TEST
#


def test_map_summary(new_mapper: ProjectMapper):
    new_project = project_helper.create()
    new_project.start_date = parser.parse(new_project.start_date)
    new_project.end_date = parser.parse(new_project.end_date)
    dto = new_mapper.entity_to_summary(new_project)

    assert new_project.name == dto['name']
    assert len(dto) == 4


def test_entity_to_details(new_mapper: ProjectMapper):
    new_project = project_helper.create()
    new_project.start_date = parser.parse(new_project.start_date)
    new_project.end_date = parser.parse(new_project.end_date)
    dto = new_mapper.entity_to_details(new_project)

    assert new_project.name == dto['name']
    assert new_project.description == dto['description']
    assert 'created_at' in dto
    assert 'updated_at' in dto


#
#   VALIDATION TEST
#


def test_create_validate_success_maximal_data(new_mapper: ProjectMapper):
    try:
        data = new_mapper.body_to_create_dto({
            "name": project_helper.name,
            "description": project_helper.description,
            "start_date": project_helper.start_date,
            "end_date": project_helper.end_date,
            "main_user_id": 1,
            "institution_id": 2,
        })

        assert data['name'] == project_helper.name
        assert data['description'] == project_helper.description
        assert data['main_user_id'] == 1
        assert data['institution_id'] == 2
    except InputValidationError:
        assert False


def test_create_validate_success_minimal_data(new_mapper: ProjectMapper):
    try:
        data = new_mapper.body_to_create_dto({
            "name": project_helper.name,
            "start_date": project_helper.start_date,
            "end_date": project_helper.end_date,
            "main_user_id": 1,
            "institution_id": 2,
        })

        assert data['name'] == project_helper.name
        assert data['main_user_id'] == 1
        assert data['institution_id'] == 2
    except InputValidationError:
        assert False


def test_create_validate_fail_by_name_missing(new_mapper: ProjectMapper):
    try:
        new_mapper.body_to_create_dto({
            "start_date": project_helper.start_date,
            "end_date": project_helper.end_date,
            "main_user_id": 1,
            "institution_id": 2,
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_start_missing(new_mapper: ProjectMapper):
    try:
        new_mapper.body_to_create_dto({
            "name": project_helper.name,
            "end_date": project_helper.end_date,
            "main_user_id": 1,
            "institution_id": 2,
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_end_missing(new_mapper: ProjectMapper):
    try:
        new_mapper.body_to_create_dto({
            "name": project_helper.name,
            "start_date": project_helper.start_date,
            "main_user_id": 1,
            "institution_id": 2,
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_user_missing(new_mapper: ProjectMapper):
    try:
        new_mapper.body_to_create_dto({
            "name": project_helper.name,
            "start_date": project_helper.start_date,
            "end_date": project_helper.end_date,
            "institution_id": 2,
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_institution_missing(new_mapper: ProjectMapper):
    try:
        new_mapper.body_to_create_dto({
            "name": project_helper.name,
            "start_date": project_helper.start_date,
            "end_date": project_helper.end_date,
            "main_user_id": 1,
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_error_field(new_mapper: ProjectMapper):
    try:
        new_mapper.body_to_create_dto({
            "name": project_helper.name,
            "start_date": project_helper.start_date,
            "end_date": project_helper.end_date,
            "main_user_id": 1,
            "institution_id": 2,
            'description2': ''
        })
        assert False
    except InputValidationError:
        pass


def test_update_validate_success_maximal_data(new_mapper: ProjectMapper):
    try:
        data = new_mapper.body_to_update_dto({
            "name": project_helper.name,
            "description": project_helper.description,
            "start_date": project_helper.start_date,
            "end_date": project_helper.end_date,
            "main_user_id": 1,
            "institution_id": 2,
        })

        assert data['name'] == project_helper.name
        assert data['description'] == project_helper.description
        assert data['main_user_id'] == 1
        assert data['institution_id'] == 2
    except InputValidationError:
        assert False


def test_update_validate_success_minimal_data(new_mapper: ProjectMapper):
    try:
        data = new_mapper.body_to_update_dto({
        })

        assert data['name'] == None
        assert data['description'] == None
        assert data['main_user_id'] == None
        assert data['institution_id'] == None
    except InputValidationError:
        assert False


def test_update_validate_fail_by_error_field(new_mapper: ProjectMapper):
    try:
        new_mapper.body_to_update_dto({
            'description2': ''
        })
        assert False
    except InputValidationError:
        pass
