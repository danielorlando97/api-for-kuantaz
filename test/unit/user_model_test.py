from src.user.model import UserModel
import pytest
from src.user.dtos_mapper import UserMapper
from src.core.api_errors import InputValidationError
from dateutil import relativedelta, parser
import tools.user as user_helper


@pytest.fixture(scope='module')
def new_mapper():
    return UserMapper()

#
#   MODEL TEST
#


def test_create_model():
    new_user = user_helper.create()

    assert new_user.name == user_helper.name
    assert new_user.last_name == user_helper.last_name
    assert new_user.office == user_helper.office
    assert new_user.rut == user_helper.rut
    assert new_user.age == -1
    assert new_user.birthday == user_helper.birthday


#
#   VIEW TEST
#


def test_map_summary(new_mapper: UserMapper):
    new_user = user_helper.create()

    dto = new_mapper.entity_to_summary(new_user)

    assert new_user.name == dto['name']
    assert new_user.last_name == dto['last_name']
    assert new_user.age == dto['age']
    assert new_user.office == dto['office']
    assert len(dto) == 5


def test_entity_to_details(new_mapper: UserMapper):
    new_user = user_helper.create()
    new_user.birthday = parser.parse(new_user.birthday)
    dto = new_mapper.entity_to_details(new_user)

    assert new_user.name == dto['name']
    assert new_user.last_name == dto['last_name']
    assert new_user.age == dto['age']
    assert new_user.office == dto['office']
    assert new_user.rut == dto['rut']
    assert 'created_at' in dto
    assert 'updated_at' in dto

    assert type(dto['projects']) == list


def test_entity_to_rut_view(new_mapper: UserMapper):
    new_user = user_helper.create()

    dto = new_mapper.entity_to_rut_view(new_user)

    assert new_user.name == dto['name']
    assert new_user.last_name == dto['last_name']
    assert new_user.age == dto['age']
    assert new_user.office == dto['office']
    assert new_user.rut == dto['rut']

    assert type(dto['projects']) == list


#
#   VALIDATION TEST
#


def test_create_validate_success_maximal_data(new_mapper: UserMapper):
    try:
        data = new_mapper.body_to_create_dto({
            'name': user_helper.name,
            'last_name': user_helper.last_name,
            'rut': user_helper.rut,
            'birthday': user_helper.birthday,
            'office': user_helper.office

        })

        assert data['name'] == user_helper.name
        assert data['last_name'] == user_helper.last_name
        assert data['rut'] == user_helper.rut
        assert data['birthday'] == user_helper.birthday
        assert data['office'] == user_helper.office
    except InputValidationError:
        assert False


def test_create_validate_fail_by_name_missing(new_mapper: UserMapper):
    try:
        new_mapper.body_to_create_dto({
            'last_name': user_helper.last_name,
            'rut': user_helper.rut,
            'birthday': user_helper.birthday,
            'office': user_helper.office
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_last_name_missing(new_mapper: UserMapper):
    try:
        new_mapper.body_to_create_dto({
            'name': user_helper.name,
            'rut': user_helper.rut,
            'birthday': user_helper.birthday,
            'office': user_helper.office
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_rut_missing(new_mapper: UserMapper):
    try:
        new_mapper.body_to_create_dto({
            'name': user_helper.name,
            'last_name': user_helper.last_name,
            'birthday': user_helper.birthday,
            'office': user_helper.office
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_birthday_missing(new_mapper: UserMapper):
    try:
        new_mapper.body_to_create_dto({
            'name': user_helper.name,
            'last_name': user_helper.last_name,
            'rut': user_helper.rut,
            'office': user_helper.office
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_office_missing(new_mapper: UserMapper):
    try:
        new_mapper.body_to_create_dto({
            'name': user_helper.name,
            'last_name': user_helper.last_name,
            'rut': user_helper.rut,
            'birthday': user_helper.birthday,
        })

        assert False

    except InputValidationError:
        pass


def test_create_validate_fail_by_error_field(new_mapper: UserMapper):
    try:
        data = new_mapper.body_to_create_dto({
            'name': user_helper.name,
            'last_name': user_helper.last_name,
            'rut': user_helper.rut,
            'birthday': user_helper.birthday,
            'office': user_helper.office,
            'description': ""

        })
        assert False
    except InputValidationError:
        pass


def test_update_validate_success_maximal_data(new_mapper: UserMapper):
    try:
        data = new_mapper.body_to_update_dto({
            'name': user_helper.name,
            'last_name': user_helper.last_name,
            'rut': user_helper.rut,
            'birthday': user_helper.birthday,
            'office': user_helper.office

        })

        assert data['name'] == user_helper.name
        assert data['last_name'] == user_helper.last_name
        assert data['rut'] == user_helper.rut
        assert data['birthday'] == user_helper.birthday
        assert data['office'] == user_helper.office
    except InputValidationError:
        assert False


def test_update_validate_success_minimal_data(new_mapper: UserMapper):
    try:
        data = new_mapper.body_to_update_dto({
        })

        assert data['name'] == None
        assert data['last_name'] == None
        assert data['rut'] == None
        assert data['birthday'] == None
        assert data['office'] == None
    except InputValidationError:
        assert False


def test_update_validate_fail_by_error_field(new_mapper: UserMapper):
    try:
        new_mapper.body_to_update_dto({
            'description2': ''
        })
        assert False
    except InputValidationError:
        pass
