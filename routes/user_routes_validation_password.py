from cerberus import Validator
from flask import request


from ._validator import validator
from .user_routes_validation import _password


def validate_password_update(password):
    _password_update = {
        **_password,
        "required": True,
        "nullable": False,
    }
    v_object = {
        "password": password
    }
    v_schema = {
        "password": _password_update
    }

    # Run validation
    validator(request, v_schema, v_object)
