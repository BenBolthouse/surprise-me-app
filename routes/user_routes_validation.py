from ._route_decorator import RouteDecorator
from ._validator import validator

# Validator schemas
_password = {
    "required": True,
    "nullable": False,
    "minlength": 8,
    "maxlength": 32,
    "type": "string",
    "regex": "^(?!.*\ )(?=.*\d)(?=.+\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,32}$",  # noqa
}
_firstName = {
    "required": True,
    "nullable": False,
    "minlength": 1,
    "maxlength": 32,
    "regex": "^([A-Za-z'-]+)$",  # noqa
}
_lastName = {
    "required": True,
    "nullable": False,
    "minlength": 1,
    "maxlength": 32,
    "regex": "^([A-Za-z'-]+)$",  # noqa
}
_email = {
    "required": True,
    "nullable": False,
    "minlength": 5,
    "maxlength": 128,
    "type": "string",
    "regex": '^(?:(?:[\w`~!#$%^&*\-=+;:{}\'|,?\/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}\'|,?\/]+))*\.[\w`~!#$%^&*\-=+;:{}\'|,?\/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d\-]+(?:\.[a-zA-Z\d\-]+)*|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])$',  # noqa
}
_shareLocation = {
    "required": True,
    "nullable": False,
    "type": "boolean"
}
_coordLat = {
    "required": True,
    "nullable": False,
    "type": "string",
    "regex": "^(?=.*[0-9]).{3,3}\.(?=.*[0-9]).{6,6}$",  # noqa
}
_coordLong = {
    "required": True,
    "nullable": False,
    "type": "string",
    "regex": "^(?=.*[0-9]).{2,2}\.(?=.*[0-9]).{6,6}$",  # noqa
}


def _on_create(request):
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
        "password": _password,
        "firstName": _firstName,
        "lastName": _lastName,
        "email": _email,
        "shareLocation": _shareLocation,
        "coordLat": _coordLat,
        "coordLong": _coordLong,
    }

    # Pass exception if validation failed and add errors to request
    try:
        request = validator(request, v_schema, v_object)
    except Exception as e:
        pass


user_validate_on_create = RouteDecorator(req=_on_create)
