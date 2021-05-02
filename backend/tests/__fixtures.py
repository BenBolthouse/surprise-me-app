from datetime import datetime
from flask_migrate import upgrade, downgrade
from os import path
import json
import pytest
import os

from app import app
from models import db, User, Connection, Message
from seed import test, down
import models


@pytest.fixture(scope="session")
def seed():
    '''
    Seeds the test database; scoped to session.
    '''
    # Get the migration directory because it doesn't exist in the root
    # directory. Pytest will look at the root directory by default.
    migrations_directory = path.join(path.dirname(models.__file__), "..", "migrations")

    with app.test_client() as client:
        with app.app_context():
            # Run any available upgrades from models migration, ...
            upgrade(directory=migrations_directory)
            # Try to delete all of the records and reset sequences to 1, ...
            down()
            # Seed the test database, ...
            test()

            yield
            # Finally, undo all seed data on cleanup.
            down()


@pytest.fixture(scope="session")
def client():
    '''
    Sets up a client to which http requests can be sent; scoped to session.
    '''
    # white tests are running ignore require login
    app.login_manager.session_protection = None

    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope="session")
def headers(client):
    '''
    Sets headers for http requests, including CSRF protection token; scoped to
    session.
    '''
    # Endpoint should provide a unique CSRF token upon each request.
    response = client.get("/api/v1/csrf_token")

    yield {
        "Content-Type": "application/json",
        "Allow": "application/json",
        "X-CSRFToken": response.json.get("data"),
    }


@pytest.fixture(scope="session")
def login(client, headers):
    '''
    Logs a user in; scoped to session.
    '''
    def a(email):
        # Endpoint should allow for a session to be posted with correct user
        # credentials and a valid CSRF token.
        endpoint = "/api/v1/sessions"
        data = {
            "email": email,
            "password": "Password1234$",
        }
        client.post(
            endpoint,
            data=json.dumps(data),
            headers=headers)

    yield a
