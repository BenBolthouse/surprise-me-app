from datetime import datetime


from .__fixtures import seed, client, headers, login
from config import Config
from models import Connection, Notification


def test__connections_routes__GET___retrieve_by_range(seed, client, headers, login):
    # Arrange
    start = "2021-10-10T12:10:00:000000"
    url = f"/api/v1/connections/1/messages?start={start}"

    # Act
    login = login("D@email.com")
    response = client.get(url, headers=headers)

    # Assert from response
    json = response.json.get
    assert json("message") == "Success"
    assert response.status_code == 200
    assert len(json("data")) == 6


def test__connections_routes__GET___retrieve_by_range(seed, client, headers, login):
    # Arrange
    end = "2021-10-10T12:10:00:000000"
    url = f"/api/v1/connections/1/messages?end={end}"

    # Act
    login = login("D@email.com")
    response = client.get(url, headers=headers)

    # Assert from response
    json = response.json.get
    assert json("message") == "Success"
    assert response.status_code == 200
    assert len(json("data")) == 9


def test__connections_routes__GET___retrieve_by_range(seed, client, headers, login):
    # Arrange
    start = "2021-10-10T12:10:00:000000"
    end = "2021-10-10T12:10:00:000000"
    url = f"/api/v1/connections/1/messages?start={start}&end={end}"

    # Act
    login = login("D@email.com")
    response = client.get(url, headers=headers)

    # Assert from response
    json = response.json.get
    messages = json("data")
    assert json("message") == "Success"
    assert response.status_code == 200
    assert len(messages) == 6
