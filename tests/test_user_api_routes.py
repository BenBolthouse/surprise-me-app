from copy import deepcopy
import json
import pytest

from models import db, User
from app import app


@pytest.fixture(scope="module")
def client(request):

    # Yield the application context
    print("Run startup...")
    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            yield client

            # Remove all data from all tables and reset auto increment
            print("Run teardown...")
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                print('Clear table %s' % table)
                db.engine.execute(table.delete())
                db.engine.execute("ALTER SEQUENCE %s_id_seq RESTART WITH 1;" % table)  # noqa
            db.session.commit()


def test_post_new_user(client):
    # Arrangement
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Allow": mimetype,
    }
    url = "/api/users"
    data = {
        "password": "Du&&?121",
        "firstName": "Demo",
        "lastName": "User",
        "email": "demoUser@email.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456
    }

    # Expected results
    status_code = 201
    message = "success"
    expected_data = {
        "id": 1,
        "firstName": "Demo",
        "lastName": "User",
        "email": "demoUser@email.com",
        "shareLocation": True,
        "coordLat": "123.123456",
        "coordLong": "12.123456"
    }

    # Action
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == status_code
    assert response.json["message"] == message
    assert response.json["data"] == expected_data


def test_post_user_with_identical_email(client):
    # Arrangement
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Allow": mimetype,
    }
    url = "/api/users"
    data = {
        "password": "Du&&?121",
        "firstName": "Demo",
        "lastName": "User",
        "email": "demoUser@email.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456
    }

    # Expected results
    status_code = 400
    message = "requested_email_is_in_use"
    expected_data = {
        "details": "The email demoUser@email.com is already in use."
    }

    # Action
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == status_code
    assert response.json["message"] == message
    assert response.json["data"] == expected_data


def test_post_user_with_invalid_names(client):
    # Arrangement
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Allow": mimetype,
    }
    url = "/api/users"
    data = {
        "password": "Du&&?121",
        "firstName": "Demo",
        "lastName": "User",
        "email": "demoUser2@email.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456
    }

    # Action 1
    test_1 = deepcopy(data)
    test_1["first_name"] = "%BADNAME%"
    test_1["last_name"] = "%BADNAME%"
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == 400
    assert response.json["message"] == "valdation_errors"
    assert response.json["data"] == {
        "first_name": ["Name contains illegal characters."],
        "last_name": ["Name contains illegal characters."]
    }
