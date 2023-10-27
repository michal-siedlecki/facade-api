import json


def test_post_request(client, data, api_token):
    response = client.post("/", json=data, headers={"X_API_TOKEN": api_token})
    response_value = list(json.loads(response.content).values())[0]
    response_value_data = list(response_value.values())[0]
    assert response.status_code == 200
    assert response_value_data == list(data.values())[0]
