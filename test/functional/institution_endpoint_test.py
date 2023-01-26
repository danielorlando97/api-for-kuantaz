from src.institution.model import InstitutionModel
from src.project.model import ProjectModel
from src.user.model import UserModel
from src import db
import pytest
import tools.institutions as inst_helper
import tools.project as proj_helper
import tools.user as user_helper


#
#   QUERY TEST
#

def test_success_get(test_client):
    new_institution = inst_helper.create()

    db.session.add(new_institution)
    db.session.commit()

    response = test_client.get("/institution")

    assert response.status_code == 200
    assert response.json['count'] == 1
    assert type(response.json['data']) == list
    assert len(response.json['data']) == 1

    db_entity = response.json['data'][0]
    assert db_entity['name'] == new_institution.name
    assert db_entity['description'] == new_institution.description
    assert db_entity['direction'] == new_institution.direction

    db.session.delete(new_institution)
    db.session.commit()


def test_success_get_directions(test_client):
    new_institution = inst_helper.create()

    db.session.add(new_institution)
    db.session.commit()

    response = test_client.get("/institutions/direction")

    assert response.status_code == 200
    assert response.json['count'] == 1
    assert type(response.json['data']) == list
    assert len(response.json['data']) == 1

    db_entity = response.json['data'][0]
    assert db_entity['name'] == new_institution.name[:3].upper()
    assert db_entity['direction'] == f'https://www.google.com/maps/search/{new_institution.direction}'

    db.session.delete(new_institution)
    db.session.commit()


def test_success_get_by_id(test_client):
    new_institution = inst_helper.create()
    db.session.add(new_institution)

    new_user = user_helper.create()
    db.session.add(new_user)
    db.session.commit()

    new_project = proj_helper.create(new_user.id, new_institution.id)
    db.session.add(new_project)
    db.session.commit()

    response = test_client.get(f"/institution/{new_institution.id}")

    assert response.status_code == 200
    assert response.json['entity'] != None

    db_entity = response.json['entity']
    assert db_entity['name'] == new_institution.name
    assert db_entity['description'] == new_institution.description
    assert db_entity['direction'] == new_institution.direction
    assert len(db_entity['projects']) == 1
    assert db_entity['projects'][0]['id'] == new_project.id
    assert db_entity['projects'][0]['main_user']['id'] == new_user.id

    db.session.delete(new_project)
    db.session.delete(new_institution)
    db.session.delete(new_user)
    db.session.commit()


#
#   COMMAND TEST
#

def test_success_create(test_client):
    new_institution = inst_helper.create()
    response = test_client.post("/institution", json={
        'name': new_institution.name
    })

    assert response.status_code == 200
    assert type(response.json['entity_id']) == int

    entity = InstitutionModel.query.get_or_404(response.json['entity_id'])

    assert entity.name == new_institution.name

    db.session.delete(entity)
    db.session.commit()


def test_fail_create(test_client):
    response = test_client.post("/institution", json={})

    assert response.status_code == 400

    data = InstitutionModel.query.all()

    assert len(data) == 0


def test_success_delete(test_client):
    new_institution = inst_helper.create()
    db.session.add(new_institution)
    db.session.commit()

    response = test_client.delete(f"/institution/{new_institution.id}")
    assert response.status_code == 200

    data = InstitutionModel.query.all()

    assert len(data) == 0


def test_success_update(test_client):
    new_institution = inst_helper.create()
    db.session.add(new_institution)
    db.session.commit()

    response = test_client.put(f"/institution/{new_institution.id}", json={
        'name': "New_name",
        'description': "New_description",
        'direction': 'New_direction'
    })

    assert response.status_code == 200

    entity = InstitutionModel.query.get_or_404(new_institution.id)

    assert entity.name == "New_name"
    assert entity.description == "New_description"
    assert entity.direction == "New_direction"

    db.session.delete(entity)
    db.session.commit()
