from flask import request, make_response
from functools import wraps


class RouteDecorator:
    """ Returns a Flask route decorator.

    Callback function `req` takes parameter `request` to access
    the request context.

    Callback function `res` takes parameter `response` to access
    the response. """

    def __init__(self, req=None, res=None):
        self._req = req
        self._res = res

    def _decorator(self):
        def _dec(func):
            @wraps(func)
            def __dec(*args, **kwargs):
                if self._req:
                    self._req(request)
                result = func(*args, **kwargs)
                response = make_response(result)
                if self._res:
                    self._res(response)
                return result
            return __dec
        return _dec

    def __call__(self):
        return self._decorator()
