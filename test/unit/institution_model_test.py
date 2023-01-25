from src.institution.model import InstitutionModel
import pytest
from src.institution.dtos_mapper import InstitutionMapper

name = 'Institution'
description = "A fine place"
direction = '32 C/ A and B'


@pytest.fixture(scope='module')
def new_institution():
    return InstitutionModel(name, description, direction)


@pytest.fixture(scope='module')
def new_mapper():
    return InstitutionMapper()


def test_create_model(new_institution: InstitutionModel):
    assert new_institution.name == name
    assert new_institution.description == description
    assert new_institution.direction == direction


def test_map_summary(new_institution: InstitutionModel, new_mapper: InstitutionMapper):
    dto = new_mapper.entity_to_summary(new_institution)

    assert new_institution.name == dto['name']
    assert new_institution.description == dto['description']
    assert new_institution.direction == dto['direction']
