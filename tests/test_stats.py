import json
from unittest.mock import Mock, MagicMock, patch

result = {
        "subscribed_at": "2020-04-27 17:57:29.857738",
        "user_id": "b72159fe-67d8-4ea7-8313-af2bf9210799",
        "user_name": "julietezekwe",
        "dataset_id": "b72159fe-67d8-4ea7-8313-af2bf9210799",
        "dataset_name": "new dataset",
    }

@patch('data_subscriptions.api.resources.stat.prepare_stat', MagicMock(return_value=result))
def test_get_subscription_200_subscription_exists(client, all_subscription):
  # Return 200 OK when json is returned and all keys present
    response = client.get(f"/api/v1/stat")
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data.keys()
    assert isinstance(data["result"], list) is True
    assert "user_name" in data["result"][0].keys()
    assert "dataset_name" in data["result"][0].keys()
    assert "user_id" in data["result"][0].keys()
    assert "dataset_id" in data["result"][0].keys()
    assert "subscribed_at" in data["result"][0].keys()

def test_get_subscription_200_subscription_exists(client, all_subscription):
    # Return 200 OK when csv is returned
    response = client.get(f"/api/v1/stat?download=yes")
    assert response.status_code == 200
    data = response
    print(str(response))
