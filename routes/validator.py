from cerberus import Validator


from .route_decorator import RouteDecorator


def validator(request, v_schema, v_object):
    validator = Validator(v_schema)

    request.validation_result = validator.validate(v_object)
    request.validation_errors = validator.errors

    return request
