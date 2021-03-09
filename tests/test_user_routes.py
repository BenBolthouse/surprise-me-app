from copy import deepcopy
import json
import pytest


from ._fixtures import client, headers
from ._fixtures import database_user_a, database_user_a_login
from ._fixtures import database_user_b, database_user_b_login


from models import db, User
from app import app


def test_a_1_post_user_succeeds(
        client,
        headers,
        database_user_a):

    # Arrangement
    user = User.get_by_id(1)

    # Database assertions
    assert user.to_json_on_create() == {
        "id": 1,
        "firstName": "Demo",
        "lastName": "User",
        "email": "database_user_a@example.com",
        "shareLocation": True,
        "coordLat": "123.123456",
        "coordLong": "12.123456"
    }


def test_a_2_post_user_fails_with_identical_email(
        client,
        headers,
        database_user_a):

    # Arrangement
    url = "/api/users"
    data = deepcopy(database_user_a)

    # Action
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == 400
    assert response.json["message"] == "The requested email is in use."


def test_a_3_post_user_fails_with_invalid_email(
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
        assert response.json["message"] == "Data validation failed"
        assert "not match regex" in response.json["data"]["email"][0]


def test_a_4_post_user_fails_with_invalid_password(
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

    for password in test_subjects:
        # Arrange
        data = deepcopy(database_user_a)
        data["password"] = password

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "Data validation failed"
        assert "not match regex" in response.json["data"]["password"][0]

    # Test for short passwords

    # Arrange
    data = deepcopy(database_user_a)
    data["password"] = "2short%"

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Data validation failed"
    assert "min length" in response.json["data"]["password"][0]

    # Test for long passwords

    # Arrange
    data["password"] = "4%-too-Long-too-Long-too-Long-too-Long"  # noqa

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Data validation failed"
    assert "max length" in response.json["data"]["password"][0]


def test_a_5_post_user_fails_with_invalid_geocoords(
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

    for coordLat in test_subjects:
        # Arrange
        data = deepcopy(database_user_a)
        data["coordLat"] = coordLat
        data["coordLong"] = coordLat

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "Data validation failed"
        assert "not match regex" in response.json["data"]["coordLat"][0]
        assert "not match regex" in response.json["data"]["coordLong"][0]


def test_a_6_post_user_fails_with_invalid_names(
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

    for name in test_subjects:
        # Arrange
        data = deepcopy(database_user_a)
        data["firstName"] = name
        data["lastName"] = name

        # Act
        response = client.post(url, data=json.dumps(data), headers=headers)

        # Assert
        assert response.status_code == 400
        assert response.json["message"] == "Data validation failed"  # noqa
        assert "not match regex" in response.json["data"]["firstName"][0]
        assert "not match regex" in response.json["data"]["lastName"][0]


def test_b_1_patch_user_succeeds(
        client,
        headers,
        database_user_a,
        database_user_a_login):

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
        response = client.patch(
            url,
            data=json.dumps({data[0]: data[1]}),
            headers=headers)

        # Expected results
        status_code = 200
        message = "success"

        # Assert
        response_data = response.json.get("data")
        assert response.status_code == 200
        assert response.json["message"] == "Success"
        assert response_data[data[0]] == data[1]


def test_c_1_post_user_session_succeeds(
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


def test_c_2_post_user_session_fails_unknown_email(
        client,
        headers,
        database_user_a):

    # Arrange
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": "wrong_email@email.com",
    }

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 404
    assert response.json["message"] == "A user was not found with the provided email."  # noqa


def test_c_3_post_user_session_fails_invalid_password(
        client,
        headers,
        database_user_a):

    # Arrange
    url = "/api/sessions"
    data = {
        "password": "wrong_password",
        "email": database_user_a["email"],
    }

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Password is incorrect."


def test_b_2_patch_user_fails_email_conflict(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login):

    # Arrange
    url = "/api/users"
    data = {
        "email": "database_user_b@example.com"
    }

    # Act
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 400
    assert response.json.get("message") == "The requested email is in use."


def test_d_1_get_session_user_succeeds(
        client,
        headers,
        database_user_a,
        database_user_a_login):

    # Arrangement
    url = "/api/users"

    # Action
    response = client.get(url, headers=headers)

    # Response assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == {
        "id": 1,
        "firstName": "Demo",
        "lastName": "User",
        "email": "database_user_a@example.com",
        "shareLocation": True,
        "coordLat": "123.123456",
        "coordLong": "12.123456"
    }
