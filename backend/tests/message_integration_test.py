from datetime import datetime


from .__fixtures import seed, client, headers, login
from config import Config
from models import Connection, Notification


def test__connections_routes__GET___retrieve(seed, client, headers, login):
    # Arrange
    url = "/api/v1/connections/1/messages"
    body = {
        "type": "message",
        "body": "Hello world",
    }

    # Act
    login = login("D@email.com")
    response = client.get(url, headers=headers)

    # Assert from response
    json = response.json.get
    assert json("message") == "Success"
    assert response.status_code == 201

    # Assert from database
