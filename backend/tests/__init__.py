from datetime import datetime
from flask_migrate import upgrade, downgrade
import json
import pytest
import os

from app import app
from models import db, User, UserConnection, ChatMessage
from seed import seed_test, seed_undo


@pytest.fixture(scope="session")
def seed():
    """
    Seeds the test database; scoped to session.
    """
    with app.test_client() as client:
        with app.app_context():
            # First run a seed undo to catch old records from any failed test
            # runs, ...
            seed_undo()
            # Perform any pending migrations before seeding, ...
            upgrade()
            # Seed the test database, ...
            seed_test()
            # Yield with no context, ...
            yield
            # Finally, undo all seed data on cleanup.
            seed_undo()


@pytest.fixture(scope="session")
def http_client():
    """
    Sets up a client to which http requests can be sent; scoped to session.
    """
    with app.test_client() as client:
        with app.app_context():
            # Yield the client
            yield client


@pytest.fixture(scope="session")
def http_headers(http_client):
    """
    Sets headers for http requests, including CSRF protection token; scoped to
    session.
    """
    # Endpoint should provide a unique CSRF token upon each request.
    response = http_client.get("/api/csrf")
    yield {
        "Content-Type": "application/json",
        "Allow": "application/json",
        "X-CSRFToken": response.json.get("data")["token"]
    }


@pytest.fixture(scope="session")
def user_login(http_client, http_headers):
    """
    Logs a user in; scoped to session.
    """
    def login(user_email):
        # Endpoint should allow for a session to be posted with correct user
        # credentials and a valid CSRF token.
        endpoint = "/api/sessions"
        data = {
            "email": user_email,
            "password": "Password1234$",
        }
        http_client.post(
            endpoint,
            data=json.dumps(data),
            headers=http_headers
        )

    yield login
