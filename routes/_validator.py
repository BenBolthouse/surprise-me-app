from cerberus import Validator
from werkzeug.exceptions import BadRequest

from ._route_decorator import RouteDecorator


def validator(request, v_schema, v_object):
    """ Loads validation results onto the request object.

    Dictionary `v_object` contains values for validation.

    Dictionary `v_schema` contains cerberus validation rules. """

    # Scoped for try except block
    validator = None

    # Raise exception for anything that cerberus can't eat
    try:
        validator = Validator(v_schema)
    except Exception as e:
        raise Exception("Schema format error")

    # Do the validation and add results to the request
    if not validator.validate(v_object):
        raise BadRequest(response={
            "message": "Data validation failed",
            "data": validator.errors
        })

    return request
