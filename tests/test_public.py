import json


def test_post_request(client, data, user_token):
    response = client.post("/", json=data, headers={"X-API-HEADER": user_token})
    response_value = list(json.loads(response.content).values())[0]
    response_value_data = list(response_value.values())[0]
    assert response.status_code == 200
    assert response_value_data == list(data.values())[0]


def test_post_request_wrong_token(client, data, api_token):
    response = client.post("/", json=data, headers={"X-API-HEADER": "bad_token"})
    assert response.status_code == 403


def test_post_request_no_token(client, data, api_token):
    response = client.post("/", json=data)
    assert response.status_code == 403
