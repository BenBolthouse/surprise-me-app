from copy import deepcopy
import json
import pytest


from ._utilities import client, headers
from ._utilities import database_seed_demo_users, login_client


from models import db, User


# * ===========================================================================
# * POST
# * ===========================================================================


def test_user_post_success_yields_user_data(
        client, headers):
    """
    Assert formatted json response for
    addition of a demo user.
    """
    # Arrange
    url = "/api/users"
    user_template = {
        "password": "Password1234$",
        "firstName": "Ida",
        "lastName": "Iratemouth",
        "email": "database_user_i@example.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456,
    }
    # Act
    response = client.post(
        url,
        data=json.dumps(user_template),
        headers=headers)
    response_message = response.json.get("message")
    response_data = response.json.get("data")
    # Assert
    assert response_message == "Success"
    assert response_data == {
        "id": 9,
        "firstName": response_data["firstName"],
        "lastName": response_data["lastName"],
        "email": response_data["email"],
        "shareLocation": response_data["shareLocation"],
    }


def test_user_login_failed_unknown_email(
        client, headers):
    """
    Assert application rejects invalid
    requests for login.
    """
    # Act
    url = "/api/sessions"
    login_request_body = {
        "password": "Password1234$",
        "email": "database_user_z@example.com",
    }
    # Assert
    response = client.post(
        url,
        data=json.dumps(login_request_body),
        headers=headers)
    # Assertions
    assert response.status_code == 404
    assert response.json.get("message") == "A user was not found with the provided email."  # noqa


def test_user_login_failed_invalid_password(
        client, headers):
    """
    Assert application rejects invalid
    requests for login.
    """
    # Act
    url = "/api/sessions"
    login_request_body = {
        "password": "BAD-Password1234$",
        "email": "database_user_a@example.com",
    }
    # Assert
    response = client.post(
        url,
        data=json.dumps(login_request_body),
        headers=headers)
    # Assertions
    assert response.status_code == 400
    assert response.json.get("message") == "Password is incorrect."  # noqa


def test_user_post_failed_email_taken(
        client, headers, login_client):
    """
    Assert non-unique emails are rejected on
    user POST.
    """
    # Arrange
    url = "/api/users"
    user_template = {
        "password": "Password1234$",
        "firstName": "Emily",
        "lastName": "Earwhisper",
        "email": "database_user_e@example.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456,
    }
    # Act
    response = client.post(
        url,
        data=json.dumps(user_template),
        headers=headers)
    response_message = response.json.get("message")
    # Assert
    assert response_message == "The requested email is in use."


def test_user_post_failed_invalid_password(
        client, headers, login_client):
    """
    Assert invalid first names are rejected
    on user POST.
    """
    # Arrange
    invalid_passwords = [
        "no-uppercase$4",
        "NO-LOWERCASE$4",
        "NoNumbers$A",
        "NoSpecCharS4",
        "Has Spaces5%",
    ]
    url = "/api/users"
    user_template = {
        "firstName": "Frank",
        "lastName": "Furwick",
        "email": "database_user_f@example.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456,
    }
    for password in invalid_passwords:
        # Act
        user_template["password"] = password
        response = client.post(
            url,
            data=json.dumps(user_template),
            headers=headers)
        response_message = response.json.get("message")
        response_data = response.json.get("data")
        # Assert
        assert response_message == "Data validation failed."
        assert "not match regex" in response_data["password"][0]


def test_user_post_failed_invalid_first_name(
        client, headers, login_client):
    """
    Assert invalid first names are rejected
    on user POST.
    """
    # Arrange
    invalid_first_names = [
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
    url = "/api/users"
    user_template = {
        "password": "Password1234$",
        "lastName": "Furwick",
        "email": "database_user_f@example.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456,
    }
    for first_name in invalid_first_names:
        # Act
        user_template["firstName"] = first_name
        response = client.post(
            url,
            data=json.dumps(user_template),
            headers=headers)
        response_message = response.json.get("message")
        response_data = response.json.get("data")
        # Assert
        assert response_message == "Data validation failed."
        assert "not match regex" in response_data["firstName"][0]


def test_user_post_failed_invalid_last_name(
        client, headers, login_client):
    """
    Assert invalid last names are rejected
    on user POST.
    """
    # Arrange
    invalid_last_names = [
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
    url = "/api/users"
    user_template = {
        "password": "Password1234$",
        "firstName": "Frank",
        "email": "database_user_f@example.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456,
    }
    for last_name in invalid_last_names:
        # Act
        user_template["lastName"] = last_name
        response = client.post(
            url,
            data=json.dumps(user_template),
            headers=headers)
        response_message = response.json.get("message")
        response_data = response.json.get("data")
        # Assert
        assert response_message == "Data validation failed."
        assert "not match regex" in response_data["lastName"][0]


def test_user_post_failed_invalid_email(
        client, headers, login_client):
    """
    Assert invalid emails are
    rejected on user POST.
    """
    # Arrange
    invalid_emails = [
        "BAD EMAIL@EXAMPLE.COM",
        "BADEMAIL @EXAMPLE.COM",
        "BADEMAIL@ EXAMPLE.COM",
        "BADEMAIL@EXAMPLE .COM",
        "BADEMAIL@EXAMPLE. COM",
        "BADEMAIL@EXAMPLE.COM ",
    ]
    url = "/api/users"
    user_template = {
        "password": "Password1234$",
        "firstName": "Frank",
        "lastName": "Furwick",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456,
    }
    for email in invalid_emails:
        # Act
        user_template["email"] = email
        response = client.post(
            url,
            data=json.dumps(user_template),
            headers=headers)
        response_message = response.json.get("message")
        response_data = response.json.get("data")
        # Assert
        assert response_message == "Data validation failed."
        assert "not match regex" in response_data["email"][0]


def test_user_post_failed_invalid_coord_lat(
        client, headers, login_client):
    """
    Assert invalid latitude values are
    rejected on user POST.
    """
    # Arrange
    invalid_coord_lats = [
        1234567890123456,
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
    url = "/api/users"
    user_template = {
        "password": "Password1234$",
        "firstName": "Frank",
        "lastName": "Furwick",
        "email": "database_user_f@example.com",
        "shareLocation": True,
        "coordLong": 12.123456,
    }
    for coord_lat in invalid_coord_lats:
        # Act
        user_template["coordLat"] = coord_lat
        response = client.post(
            url,
            data=json.dumps(user_template),
            headers=headers)
        response_message = response.json.get("message")
        response_data = response.json.get("data")
        # Assert
        assert response_message == "Data validation failed."
        assert "not match regex" in response_data["coordLat"][0]


def test_user_post_failed_invalid_coord_long(
        client, headers, login_client):
    """
    Assert invalid longitude values are
    rejected on user POST.
    """
    # Arrange
    invalid_coord_longs = [
        1234567890123456,
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
    url = "/api/users"
    user_template = {
        "password": "Password1234$",
        "firstName": "Frank",
        "lastName": "Furwick",
        "email": "database_user_f@example.com",
        "shareLocation": True,
        "coordLat": 123.123456,
    }
    for coord_long in invalid_coord_longs:
        # Act
        user_template["coordLong"] = coord_long
        response = client.post(
            url,
            data=json.dumps(user_template),
            headers=headers)
        response_message = response.json.get("message")
        response_data = response.json.get("data")
        # Assert
        assert response_message == "Data validation failed."
        assert "not match regex" in response_data["coordLong"][0]


def test_user_login_success_yields_user_data(
        login_client, database_seed_demo_users):
    """
    Assert formatted json response for each
    demo user in `users_templates`.
    """
    id_iterator = 1
    # Arrange
    for user in database_seed_demo_users:
        # Act
        response = login_client(user["email"])
        response_message = response.json.get("message")
        response_data = response.json.get("data")
        # Assert
        assert response_message == "Success"
        assert response.json.get("data") == {
            "id": id_iterator,
            "firstName": user["first_name"],
            "lastName": user["last_name"],
            "email": user["email"],
            "shareLocation": user["share_location"],
        }
        id_iterator += 1


# * ===========================================================================
# * GET
# * ===========================================================================


def test_user_get_success_yields_user_data(
        client, headers, login_client):
    """
    Assert formatted json response for
    authenticated get requests.
    """
    # Arrange
    url = "/api/sessions"
    # Act
    login = login_client("database_user_a@example.com")
    response = client.get(
        url,
        headers=headers)
    # Assert
    response.status_code == 200
    response.json.get("message") == "Success"
    response.json.get("data") == {
        "id": 1,
        "firstName": "Angelica",
        "lastName": "Ashworthy",
        "email": "database_user_a@example.com",
        "shareLocation": True,
        "coordLat": "123.123456",
        "coordLong": "12.123456",
    }


# * ===========================================================================
# * PATCH
# * ===========================================================================


def test_user_patch_success_yields_user_data(
        client, headers, login_client):
    """
    Assert formatted json response for
    updating a user.
    """
    # Arrange
    url = "/api/users"
    patch_properties = [
        ("firstName", "Newfirstname"),
        ("lastName", "Newlastname"),
        ("email", "new_email_address@example.com"),
        ("shareLocation", False),
        ("coordLat", 321.123123),
        ("coordLong", 21.123123),
    ]
    for prop in patch_properties:
        patch_request_body = {prop[0]: prop[1]}
        # Act
        login = login_client("database_user_a@example.com")
        response = client.patch(
            url,
            data=json.dumps(patch_request_body),
            headers=headers)
        response_message = response.json.get("message")
        response_data = response.json.get("data")
        # Assert
        assert response_message == "Success"
        assert response_data == {
            "id": 1,
            "firstName": response_data["firstName"],
            "lastName": response_data["lastName"],
            "email": response_data["email"],
            "shareLocation": response_data["shareLocation"],
            "coordLat": response_data["coordLat"],
            "coordLong": response_data["coordLong"],
        }


def test_user_patch_success_update_password(
        client, headers, login_client):
    """
    Assert formatted json response for
    updating a user.
    """
    # Arrange
    url = "/api/users"
    patch_request_body = {
        "password": "Password1234?"
    }
    # Act
    login = login_client("database_user_a@example.com")
    response = client.patch(
        url,
        data=json.dumps(patch_request_body),
        headers=headers)
    response_message = response.json.get("message")
    response_data = response.json.get("data")
    # Assert
    assert response.status_code == 200
    assert response_message == "Password updated successfully."


def test_user_patch_failed_invalid_update_password(
        client, headers, login_client):
    """
    Assert formatted json response for
    updating a user.
    """
    # Arrange
    invalid_passwords = [
        "no-uppercase$4",
        "NO-LOWERCASE$4",
        "NoNumbers$A",
        "NoSpecCharS4",
        "Has Spaces5%",
    ]
    url = "/api/users"
    login = login_client("database_user_a@example.com")
    for password in invalid_passwords:
        # Act
        patch_request_body = {"password": password}
        response = client.patch(
            url,
            data=json.dumps(patch_request_body),
            headers=headers)
        # Assert
        assert response.status_code == 400
        assert response.json.get("message") == "Data validation failed."
        assert "not match regex" in response.json.get("data")["password"][0]


def test_user_get_is_email_unique_success(
        client, headers, login_client):
    """
    Assert application detects no conflict
    email address and responds 200.
    """
    # Arrange
    url = "/api/users/is_email_unique"
    post_request_body = {
        "email": "database_user_z@example.com",
    }
    # Act
    response = client.post(
        url,
        data=json.dumps(post_request_body),
        headers=headers)
    # Assert
    assert response.status_code == 200
    assert response.json.get("message") == "Email is unique."


def test_user_get_is_email_unique_failed(
        client, headers, login_client):
    """
    Assert application detects no conflict
    email address and responds 200.
    """
    # Arrange
    url = "/api/users/is_email_unique"
    post_request_body = {
        "email": "database_user_a@example.com",
    }
    # Act
    response = client.post(
        url,
        data=json.dumps(post_request_body),
        headers=headers)
    # Assert
    assert response.status_code == 400
    assert response.json.get("message") == "Email is in use."
