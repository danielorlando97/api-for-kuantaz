
def test_success_create(test_client):
    response = test_client.post("/institution", json={
        'name': 'Institution'
    })

    print(response.json)

    assert response.status_code == 200
    assert type(response.json['entity_id']) == int
