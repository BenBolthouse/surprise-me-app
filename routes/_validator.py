from cerberus import Validator
from werkzeug.exceptions import BadRequest


def validator(request, schema, doc):

    # Scoped for try block
    validator = None

    # Raise exception for anything that cerberus can't eat
    try:
        validator = Validator(schema)
    except Exception as e:
        raise Exception("Schema format error")

    # Do the validation and add results to the request
    if not validator.validate(doc):
        raise BadRequest(response={
            "message": "Data validation failed.",
            "data": validator.errors
        })

    return request
