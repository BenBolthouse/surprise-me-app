from flask import request
from .utils import validator, RouteDecorator


required = {
    "required": True,
    "nullable": False,
}
password = {
    "nullable": True,
    "minlength": 8,
    "maxlength": 32,
    "type": "string",
    "regex": "^(?!.*\ )(?=.*\d)(?=.+\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,32}$",  # noqa
}
name = {
    "nullable": True,
    "minlength": 1,
    "maxlength": 32,
    "regex": "^([A-Za-z'-]+)$",  # noqa
}
email = {
    "nullable": True,
    "minlength": 5,
    "maxlength": 128,
    "type": "string",
    "regex": '^(?:(?:[\w`~!#$%^&*\-=+;:{}\'|,?\/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}\'|,?\/]+))*\.[\w`~!#$%^&*\-=+;:{}\'|,?\/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d\-]+(?:\.[a-zA-Z\d\-]+)*|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])$',  # noqa
}
coordinate = {
    "nullable": True,
    "type": "float",
}


def _post(req):
    target = {
        "password": req.json.get("password"),
        "first_name": req.json.get("first_name"),
        "last_name": req.json.get("last_name"),
        "email": req.json.get("email"),
        "latitude": req.json.get("latitude"),
        "longitude": req.json.get("longitude"),
    }
    schema = {
        "password": {**password, **required},
        "first_name": {**name, **required},
        "last_name": {**name, **required},
        "email": {**email, **required},
        "latitude": {**coordinate, **required},
        "longitude": {**coordinate, **required},
    }
    validator(request, schema, target)


def _patch(req):
    target = {
        "first_name": request.json.get("first_name"),
        "last_name": request.json.get("last_name"),
        "latitude": req.json.get("latitude"),
        "longitude": req.json.get("longitude"),
    }
    schema = {
        "first_name": name,
        "last_name": name,
        "latitude": coordinate,
        "longitude": coordinate,
    }
    validator(request, schema, target)


def _patch_password(req):
    target = {
        "password": request.json.get("password"),
    }
    schema = {
        "password": {**password, **required},
    }
    validator(request, schema, target)


def _patch_email(req):
    target = {
        "email": request.json.get("email"),
    }
    schema = {
        "email": {**email, **required},
    }
    validator(request, schema, target)


user_validate_on_post = RouteDecorator(req=_post)
user_validate_on_patch = RouteDecorator(req=_patch)
user_validate_on_patch_password = RouteDecorator(req=_patch_password)
user_validate_on_patch_email = RouteDecorator(req=_patch_email)
