from copy import deepcopy
import json
import pytest
import flask


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


@pytest.fixture(scope="module")
def headers(client):

    response = client.get("/api/csrf")

    yield {
        "Content-Type": "application/json",
        "Allow": "application/json",
        "X-CSRFToken": response.json["data"]["token"]
    }


user_request_template = {
    "password": "Du&&?121",
    "firstName": "Demo",
    "lastName": "User",
    "email": "demoUser@email.com",
    "shareLocation": True,
    "coordLat": 123.123456,
    "coordLong": 12.123456
}


@pytest.fixture(scope="module")
def database_user(client, headers):
    url = "/api/users"
    data = deepcopy(user_request_template)

    client.post(url, data=json.dumps(data), headers=headers)


@pytest.fixture(scope="module")
def database_user_login(client, headers, database_user):
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": "demoUser@email.com",
    }

    client.post(url, data=json.dumps(data), headers=headers)


def test_post_user_fails_with_identical_email(client, headers, database_user):
    # Arrangement
    url = "/api/users"
    data = data = deepcopy(user_request_template)

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


def test_post_user_fails_with_invalid_names(client, headers):
    # Arrangement
    url = "/api/users"
    test_subjects = [
        "%HASBADCHAR",
        "HAS&BADCHAR",
        "HASBADCHAR#",
        "5HASBADCHAR",
        "HAS9BADCHAR",
        "HASBADCHAR5",
        " HASBADCHAR",
        "HAS BADCHAR",
        "HASBADCHAR "
    ]

    # firstName
    for name in test_subjects:
        # Arrange
        data = deepcopy(user_request_template)
        data["firstName"] = name

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["firstName"][0]

    # lastName
    for name in test_subjects:
        # Arrange
        data = deepcopy(user_request_template)
        data["lastName"] = name

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["lastName"][0]


def test_post_user_fails_with_invalid_password(client, headers):
    # Arrangement
    url = "/api/users"
    test_subjects = [
        "no-uppercase$4",
        "NO-LOWERCASE$4",
        "NoNumbers$A",
        "NoSpecCharS4",
        "Has Spaces5%",
    ]

    # Regex validation tests
    for password in test_subjects:
        # Arrange
        data = deepcopy(user_request_template)
        data["password"] = password

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["password"][0]

    # Test for short passwords

    # Arrange
    data = deepcopy(user_request_template)
    data["password"] = "2short%"

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "body_data_validation_failed"
    assert "min length" in response.json["data"]["password"][0]

    # Test for long passwords

    # Arrange
    data["password"] = "4%-too-Long-too-Long-too-Long-too-Long"  # noqa

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "body_data_validation_failed"
    assert "max length" in response.json["data"]["password"][0]


def test_post_user_fails_with_invalid_email(client, headers):
    # Arrangement
    url = "/api/users"
    test_subjects = [
        "BAD EMAIL@EXAMPLE.COM",
        "BADEMAIL @EXAMPLE.COM",
        "BADEMAIL@ EXAMPLE.COM",
        "BADEMAIL@EXAMPLE .COM",
        "BADEMAIL@EXAMPLE. COM",
        "BADEMAIL@EXAMPLE.COM ",
    ]

    for email in test_subjects:
        # Arrange
        data = deepcopy(user_request_template)
        data["email"] = email

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["email"][0]


def test_post_user_fails_with_invalid_geocoords(client, headers):
    # Arrangement
    url = "/api/users"
    test_subjects = [
        1234567890123456,
        1.23456789012345,
        12.3456789012345,
        123.456789012345,
        1234.56789012345,
        12345.6789012345,
        123456.789012345,
        123,
        1234,
        12345,
        123456,
        1234567,
        12345678,
        123456789,
    ]

    # coordLat
    for coordLat in test_subjects:
        # Arrange
        data = deepcopy(user_request_template)
        data["coordLat"] = coordLat

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["coordLat"][0]

    # coordLong
    for coordLong in test_subjects:
        # Arrange
        data = deepcopy(user_request_template)
        data["coordLong"] = coordLong

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["coordLong"][0]


def test_post_user_session_succeeds(client, headers, database_user):
    # Arrange
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": "demoUser@email.com",
    }

    # Expected results
    status_code = 200
    message = "success"
    expected_data = {
        "id": 1,
        "firstName": "Demo",
        "lastName": "User",
        "email": "demoUser@email.com",
    }

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == status_code
    assert response.json["message"] == message
    assert response.json["data"] == expected_data


def test_post_user_session_fails_unknown_email(client, headers, database_user):  # noqa
    # Arrange
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": "wrong_email@email.com",
    }

    # Expected results
    status_code = 404
    message = "user_not_found"
    expected_data = {
        "details": f"A user does not exist with the email address wrong_email@email.com."  # noqa
    }

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == status_code
    assert response.json["message"] == message
    assert response.json["data"] == expected_data


def test_post_user_session_fails_invalid_password(client, headers, database_user):  # noqa
    # Arrange
    url = "/api/sessions"
    data = {
        "password": "wrong_password",
        "email": "demoUser@email.com",
    }

    # Expected results
    status_code = 400
    message = "password_is_invalid"

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == status_code
    assert response.json["message"] == message


def test_patch_user_succeeds(client, headers, database_user_login):  # noqa
    # Arrange
    url = "/api/users"
    test_subjects = [
        ("firstName", "Newfirstname"),
        ("lastName", "Newlastname"),
        ("email", "new_email_address@example.com"),
        ("shareLocation", False),
    ]

    for data in test_subjects:
        # Act
        response = client.patch(url, data=json.dumps({data[0]: data[1]}),
                                headers=headers)

        # Expected results
        status_code = 200
        message = "success"

        # Assert
        response_data = response.json.get("data")
        assert response.status_code == 200
        assert response.json["message"] == "success"
        assert response_data[data[0]] == data[1]


def test_patch_user_fails_identical_email(client, headers, database_user, database_user_login):  # noqa
    # Arrange
    url = "/api/users"
    data = {
        "email": "conflict_email@example.com"
    }
    conflict_user = deepcopy(user_request_template)
    conflict_user["email"] = "conflict_email@example.com"
    client.post(url, data=json.dumps(conflict_user), headers=headers)

    # Act
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Expected results
    status_code = 400
    message = "requested_email_is_in_use"
    expected_data = {
        "details": "The email conflict_email@example.com is already in use."  # noqa
    }

    # Assert
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert response.json.get("data") == expected_data


def test_get_session_user_succeeds(client, headers, database_user, database_user_login):  # noqa
    # Arrange
    url = "/api/users"
    test_subjects = [
        ("firstName", "Demo"),
        ("lastName", "User"),
        ("email", "demoUser@email.com"),
        ("shareLocation", True),
    ]
    for data in test_subjects:
        response = client.patch(url, data=json.dumps({data[0]: data[1]}),
                                headers=headers)

    # Act
    response = client.get(url, headers=headers)

    # Expected results
    status_code = 200
    message = "success"
    expected_data = {
        "id": 1,
        "firstName": "Demo",
        "lastName": "User",
        "email": "demoUser@email.com",
        "shareLocation": True,
        "coordLat": "123.123456",
        "coordLong": "12.123456",
    }

    # Assert
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert response.json.get("data") == expected_data
