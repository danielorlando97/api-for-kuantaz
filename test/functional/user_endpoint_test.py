
from src.user.model import UserModel
from src import db
import tools.user as inst_helper
import tools.project as proj_helper
import tools.user as user_helper


#
#   QUERY TEST
#

def test_success_get(test_client):
    new_user = inst_helper.create()

    db.session.add(new_user)
    db.session.commit()

    response = test_client.get("/user")

    assert response.status_code == 200
    assert response.json['count'] == 1
    assert type(response.json['data']) == list
    assert len(response.json['data']) == 1

    db_entity = response.json['data'][0]

    assert new_user.name == db_entity['name']
    assert new_user.last_name == db_entity['last_name']
    assert new_user.office == db_entity['office']

    db.session.delete(new_user)
    db.session.commit()


def test_success_get_by_rut(test_client):
    new_user = inst_helper.create()
    new_userA = inst_helper.create()
    new_userA.rut = '12'
    db.session.add(new_user)
    db.session.add(new_userA)
    db.session.commit()

    new_project = proj_helper.create(new_userA.id)
    db.session.add(new_project)
    db.session.commit()

    response = test_client.get("/user", query_string={'rut': '12'})

    assert response.status_code == 200
    assert response.json['count'] == 1
    assert type(response.json['data']) == list
    assert len(response.json['data']) == 1

    db_entity = response.json['data'][0]

    assert new_user.name == db_entity['name']
    assert new_user.last_name == db_entity['last_name']
    assert new_user.office == db_entity['office']
    assert db_entity['rut'] == '12'
    assert len(db_entity['projects']) == 1
    assert db_entity['projects'][0]['id'] == new_project.id

    db.session.delete(new_user)
    db.session.delete(new_project)
    db.session.delete(new_userA)
    db.session.commit()


def test_success_get_by_id(test_client):

    new_user = user_helper.create()
    db.session.add(new_user)
    db.session.commit()

    new_project = proj_helper.create(new_user.id)
    db.session.add(new_project)
    db.session.commit()

    response = test_client.get(f"/user/{new_user.id}")

    assert response.status_code == 200
    assert response.json['entity'] != None

    db_entity = response.json['entity']
    assert new_user.name == db_entity['name']
    assert new_user.last_name == db_entity['last_name']
    assert new_user.office == db_entity['office']
    assert new_user.rut == db_entity['rut']

    assert len(db_entity['projects']) == 1
    assert db_entity['projects'][0]['id'] == new_project.id

    db.session.delete(new_project)
    db.session.delete(new_user)
    db.session.commit()


#
#   COMMAND TEST
#

def test_success_create(test_client):
    new_user = inst_helper.create()
    response = test_client.post("/user", json={
        'name': user_helper.name,
        'last_name': user_helper.last_name,
        'rut': user_helper.rut,
        'birthday': user_helper.birthday,
        'office': user_helper.office
    })

    assert response.status_code == 200
    assert type(response.json['entity_id']) == int

    entity = UserModel.query.get_or_404(response.json['entity_id'])

    assert entity.name == new_user.name
    assert entity.last_name == new_user.last_name
    assert entity.rut == new_user.rut
    assert entity.office == new_user.office

    db.session.delete(entity)
    db.session.commit()


def test_fail_create(test_client):
    response = test_client.post("/user", json={})

    assert response.status_code == 400

    data = UserModel.query.all()

    assert len(data) == 0


def test_success_delete(test_client):
    new_user = inst_helper.create()
    db.session.add(new_user)
    db.session.commit()

    response = test_client.delete(f"/user/{new_user.id}")
    assert response.status_code == 200

    data = UserModel.query.all()

    assert len(data) == 0


def test_success_update(test_client):
    new_user = inst_helper.create()
    db.session.add(new_user)
    db.session.commit()

    response = test_client.put(f"/user/{new_user.id}", json={
        'name': "new",
        'last_name': "new",
        'rut': "12",
        'office': "new"
    })

    assert response.status_code == 200

    entity = UserModel.query.get_or_404(new_user.id)

    assert entity.name == 'new'
    assert entity.last_name == 'new'
    assert entity.rut == '12'
    assert entity.office == 'new'

    db.session.delete(entity)
    db.session.commit()
