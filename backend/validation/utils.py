from cerberus import Validator
from flask import make_response, request
from functools import wraps
from werkzeug.exceptions import BadRequest


def validator(request, schema, target):
    """
    Run validation using Cerberus and a given schema and target dictionary;
    raises an http exception with details when validation fails.
    """
    validator = Validator(schema)
    if not validator.validate(target):
        raise BadRequest(response={
            "message": "Data validation failed.",
            "data": validator.errors
        })
    return request


class RouteDecorator:
    """ Provides a convenient abstraction for invoking post-request &
    pre-response functions during the request response cycle, thereby allowing
    changes to the request and response states before and after the route
    logic, respectively.\\
    param `req` Callback function whose first argument is the request context\\
    param `res` Callback function whose first argument is the response context
    """
    def __init__(self, req=None, res=None):
        self.req = req
        self.res = res

    def __call__(self):
        return self._decorator()

    def _decorator(self):
        def a(func):
            @wraps(func)
            def b(*args, **kwargs):
                if self.req:
                    self.req(request)
                result = func(*args, **kwargs)
                response = make_response(result)
                if self.res:
                    self.res(response)
                return result
            return b
        return a
