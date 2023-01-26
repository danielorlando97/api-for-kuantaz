from src.project.model import ProjectModel
from src import db
import tools.institutions as int_helper
import tools.project as proj_helper
import tools.user as user_helper


#
#   QUERY TEST
#

def test_success_get(test_client):
    new_project = proj_helper.create()

    db.session.add(new_project)
    db.session.commit()

    response = test_client.get("/project")

    assert response.status_code == 200
    assert response.json['count'] == 1
    assert type(response.json['data']) == list
    assert len(response.json['data']) == 1

    db_entity = response.json['data'][0]
    assert db_entity['name'] == new_project.name

    db.session.delete(new_project)
    db.session.commit()


def test_success_get_by_id(test_client):
    new_institution = int_helper.create()
    db.session.add(new_institution)

    new_user = user_helper.create()
    db.session.add(new_user)
    db.session.commit()

    new_project = proj_helper.create(new_user.id, new_institution.id)
    db.session.add(new_project)
    db.session.commit()

    response = test_client.get(f"/project/{new_project.id}")

    assert response.status_code == 200
    assert response.json['entity'] != None

    db_entity = response.json['entity']
    assert db_entity['name'] == new_project.name
    assert db_entity['description'] == new_project.description
    assert db_entity['institution']['id'] == new_institution.id
    assert db_entity['main_user']['id'] == new_user.id

    db.session.delete(new_project)
    db.session.delete(new_institution)
    db.session.delete(new_user)
    db.session.commit()


#
#   COMMAND TEST
#

def test_success_create(test_client):

    new_institution = int_helper.create()
    db.session.add(new_institution)

    new_user = user_helper.create()
    db.session.add(new_user)
    db.session.commit()

    new_project = proj_helper.create(new_user.id, new_institution.id)

    response = test_client.post("/project", json={
        "name": new_project.name,
        "description": new_project.description,
        "start_date": new_project.start_date,
        "end_date": new_project.end_date,
        "main_user_id": new_project.main_user_id,
        "institution_id": new_project.institution_id,
    })

    assert response.status_code == 200
    assert type(response.json['entity_id']) == int

    entity = ProjectModel.query.get(response.json['entity_id'])

    assert not entity is None
    assert entity.name == new_project.name
    assert entity.description == new_project.description
    assert entity.main_user_id == new_project.main_user_id
    assert entity.institution_id == new_project.institution_id

    db.session.delete(entity)
    db.session.delete(new_institution)
    db.session.delete(new_user)
    db.session.commit()


def test_fail_create_user_error(test_client):

    new_institution = int_helper.create()
    db.session.add(new_institution)
    db.session.commit()

    new_project = proj_helper.create(None, new_institution.id)

    response = test_client.post("/project", json={
        "name": new_project.name,
        "description": new_project.description,
        "start_date": new_project.start_date,
        "end_date": new_project.end_date,
        "main_user_id": 0,
        "institution_id": new_project.institution_id,
    })

    assert response.status_code == 404

    db.session.delete(new_institution)
    db.session.commit()


def test_fail_create_institution_error(test_client):

    new_user = user_helper.create()
    db.session.add(new_user)
    db.session.commit()

    new_project = proj_helper.create(new_user.id, None)

    response = test_client.post("/project", json={
        "name": new_project.name,
        "description": new_project.description,
        "start_date": new_project.start_date,
        "end_date": new_project.end_date,
        "main_user_id": new_project.main_user_id,
        "institution_id": 0,
    })

    assert response.status_code == 404

    db.session.delete(new_user)
    db.session.commit()


def test_fail_create(test_client):
    response = test_client.post("/project", json={})

    assert response.status_code == 400

    data = ProjectModel.query.all()

    assert len(data) == 0


def test_success_delete(test_client):
    new_project = proj_helper.create()
    db.session.add(new_project)
    db.session.commit()

    response = test_client.delete(f"/project/{new_project.id}")
    assert response.status_code == 200

    data = ProjectModel.query.all()

    assert len(data) == 0


def test_success_update(test_client):
    new_project = proj_helper.create()
    db.session.add(new_project)
    db.session.commit()

    response = test_client.put(f"/project/{new_project.id}", json={
        "name": "New_name",
        "description": "New_description",
        "start_date": proj_helper.start_date,
        "end_date": proj_helper.end_date,
    })

    assert response.status_code == 200

    entity = ProjectModel.query.get(new_project.id)

    assert not entity is None
    assert entity.name == "New_name"
    assert entity.description == "New_description"

    db.session.delete(entity)
    db.session.commit()
