from .route_decorator import RouteDecorator
from .validator import validator


def on_create(request):
    v_object = {
        "password": request.json["password"],
        "firstName": request.json["firstName"],
        "lastName": request.json["lastName"],
        "email": request.json["email"],
        "shareLocation": request.json["shareLocation"],
        "coordLat": str(request.json["coordLat"]),
        "coordLong": str(request.json["coordLong"]),
    }
    v_schema = {
        "password": {
            "required": True,
            "nullable": False,
            "minlength": 8,
            "maxlength": 32,
            "regex": "^(?!.*\ )(?=.*\d)(?=.+\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,32}$",  # noqa
        },
        "firstName": {
            "required": True,
            "nullable": False,
            "minlength": 1,
            "maxlength": 32,
            "regex": "^(?!.*[\W0-9]).{0,32}$",  # noqa
        },
        "lastName": {
            "required": True,
            "nullable": False,
            "minlength": 1,
            "maxlength": 32,
            "regex": "^(?!.*[\W0-9]).{0,32}$",  # noqa
        },
        "email": {
            "required": True,
            "nullable": False,
            "minlength": 5,
            "maxlength": 128,
            "regex": '^(?:(?:[\w`~!#$%^&*\-=+;:{}\'|,?\/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}\'|,?\/]+))*\.[\w`~!#$%^&*\-=+;:{}\'|,?\/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d\-]+(?:\.[a-zA-Z\d\-]+)*|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])$',  # noqa
        },
        "shareLocation": {
            "required": True,
            "nullable": False,
            "type": "boolean"
        },
        "coordLat": {
            "required": True,
            "nullable": False,
            "type": "string",
            "regex": "^(?=.*[0-9]).{3,3}\.(?=.*[0-9]).{6,6}$",  # noqa
        },
        "coordLong": {
            "required": True,
            "nullable": False,
            "type": "string",
            "regex": "^(?=.*[0-9]).{2,2}\.(?=.*[0-9]).{6,6}$",  # noqa
        },
    }
    request = validator(request, v_schema, v_object)


user_validate_on_create = RouteDecorator(req=on_create)
