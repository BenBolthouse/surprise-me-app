from cerberus import Validator


from ._route_decorator import RouteDecorator


def validator(request, v_schema, v_object):
    """ Loads validation results onto the request object. 

    Dictionary `v_object` contains values for validation.

    Dictionary `v_schema` contains cerberus validation rules. """

    validator = Validator(v_schema)

    request.validation_result = validator.validate(v_object)
    request.validation_errors = validator.errors

    return request
