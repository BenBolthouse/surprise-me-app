from copy import deepcopy
import json
import pytest


from ._fixtures import client, headers
from ._fixtures import database_user_a, database_user_a_login


from models import db, User
from app import app


def test_post_user_fails_with_identical_email(
        client,
        headers,
        database_user_a):

    # Arrangement
    url = "/api/users"
    data = deepcopy(database_user_a)

    # Expected results
    status_code = 400
    message = "requested_email_is_in_use"
    email = database_user_a["email"]
    expected_data = {
        "details": f"The email {email} is already in use."
    }

    # Action
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == status_code
    assert response.json["message"] == message
    assert response.json["data"] == expected_data


def test_post_user_fails_with_invalid_names(
        client,
        headers,
        database_user_a):

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
        data = deepcopy(database_user_a)
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
        data = deepcopy(database_user_a)
        data["lastName"] = name

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["lastName"][0]


def test_post_user_fails_with_invalid_password(
        client,
        headers,
        database_user_a):

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
        data = deepcopy(database_user_a)
        data["password"] = password

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["password"][0]

    # Test for short passwords

    # Arrange
    data = deepcopy(database_user_a)
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


def test_post_user_fails_with_invalid_email(
        client,
        headers,
        database_user_a):

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
        data = deepcopy(database_user_a)
        data["email"] = email

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["email"][0]


def test_post_user_fails_with_invalid_geocoords(
        client,
        headers,
        database_user_a):

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
        data = deepcopy(database_user_a)
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
        data = deepcopy(database_user_a)
        data["coordLong"] = coordLong

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "body_data_validation_failed"
        assert "not match regex" in response.json["data"]["coordLong"][0]


def test_post_user_session_succeeds(
        client,
        headers,
        database_user_a):

    # Arrange
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": database_user_a["email"],
    }

    # Expected results
    status_code = 200
    message = "success"
    expected_data = {
        "id": 1,
        "firstName": "Demo",
        "lastName": "User",
        "email": database_user_a["email"],
    }

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == status_code
    assert response.json["message"] == message
    assert response.json["data"] == expected_data


def test_post_user_session_fails_unknown_email(
        client,
        headers):

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


def test_post_user_session_fails_invalid_password(
        client,
        headers,
        database_user_a):

    # Arrange
    url = "/api/sessions"
    data = {
        "password": "wrong_password",
        "email": database_user_a["email"],
    }

    # Expected results
    status_code = 400
    message = "password_is_invalid"

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == status_code
    assert response.json["message"] == message


def test_patch_user_succeeds(
        client,
        headers,
        database_user_a):

    # Arrange
    client_login = database_user_a_login(client, headers)
    url = "/api/users"
    test_subjects = [
        ("firstName", "Newfirstname"),
        ("lastName", "Newlastname"),
        ("email", "new_email_address@example.com"),
        ("shareLocation", False),
    ]

    for data in test_subjects:
        # Act
        response = client_login.patch(
            url,
            data=json.dumps({data[0]: data[1]}),
            headers=headers)

        # Expected results
        status_code = 200
        message = "success"

        # Assert
        response_data = response.json.get("data")
        assert response.status_code == 200
        assert response.json["message"] == "success"
        assert response_data[data[0]] == data[1]


def test_patch_user_fails_identical_email(
        client,
        headers,
        database_user_a):

    # Arrange
    url = "/api/users"
    data = {
        "email": "conflict_email@example.com"
    }
    conflict_user = deepcopy(database_user_a)
    conflict_user["email"] = "conflict_email@example.com"
    client.post(url, data=json.dumps(conflict_user), headers=headers)

    # Act
    client_login = database_user_a_login(client, headers)
    response = client_login.patch(url, data=json.dumps(data), headers=headers)

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


def test_get_session_user_succeeds(
        client,
        headers,
        database_user_a):

    # Arrangement
    client_login = database_user_a_login(client, headers)
    url = "/api/users"
    test_subjects = [
        ("firstName", "Demo"),
        ("lastName", "User"),
        ("email", "demoUser@email.com"),
        ("shareLocation", True),
    ]
    for data in test_subjects:
        response = client_login.patch(url, data=json.dumps({data[0]: data[1]}),
                                headers=headers)

    # Action
    response = client_login.get(url, headers=headers)

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
