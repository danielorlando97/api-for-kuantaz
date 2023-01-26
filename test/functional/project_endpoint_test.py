from src.institution.model import InstitutionModel
from src import db
import pytest
from datetime import datetime

name = 'IA'
description = 'A project'
start_date = datetime.now()
end_date = datetime.now()


# def test_success_create(test_client, new_institution):
#     response = test_client.post("/institution", json={
#         'name': new_institution.name
#     })

#     assert response.status_code == 200
#     assert type(response.json['entity_id']) == int

#     entity = InstitutionModel.query.get_or_404(response.json['entity_id'])

#     assert entity.name == new_institution.name

#     db.session.delete(entity)
#     db.session.commit()


# def test_fail_create(test_client):
#     response = test_client.post("/institution", json={})

#     assert response.status_code == 400

#     data = InstitutionModel.query.all()

#     assert len(data) == 0


# def test_success_get(test_client, new_institution):
#     db.session.add(new_institution)
#     db.session.commit()

#     response = test_client.get("/institution")

#     assert response.status_code == 200
#     assert response.json['count'] == 1
#     assert type(response.json['data']) == list
#     assert len(response.json['data']) == 1

#     db_entity = response.json['data'][0]
#     assert db_entity['name'] == new_institution.name
#     assert db_entity['description'] == new_institution.description
#     assert db_entity['direction'] == new_institution.direction

#     db.session.delete(new_institution)
#     db.session.commit()


# def test_success_get_by_id(test_client, new_institution):
#     db.session.add(new_institution)
#     db.session.commit()

#     response = test_client.get(f"/institution/{new_institution.id}")

#     assert response.status_code == 200
#     assert response.json['entity'] != None

#     db_entity = response.json['entity']
#     assert db_entity['name'] == new_institution.name
#     assert db_entity['description'] == new_institution.description
#     assert db_entity['direction'] == new_institution.direction

#     db.session.delete(new_institution)
#     db.session.commit()
