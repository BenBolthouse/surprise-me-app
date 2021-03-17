from ._route_decorator import RouteDecorator
from ._validator import validator


# ** «««««««««««««««« Rules »»»»»»»»»»»»»»»» **


_required = {
    "required": True,
    "nullable": False,
}
_password = {
    "nullable": True,
    "minlength": 8,
    "maxlength": 32,
    "type": "string",
    "regex": "^(?!.*\ )(?=.*\d)(?=.+\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,32}$",  # noqa
}
_first_name = {
    "nullable": True,
    "minlength": 1,
    "maxlength": 32,
    "regex": "^([A-Za-z'-]+)$",  # noqa
}
_last_name = {
    "nullable": True,
    "minlength": 1,
    "maxlength": 32,
    "regex": "^([A-Za-z'-]+)$",  # noqa
}
_email = {
    "nullable": True,
    "minlength": 5,
    "maxlength": 128,
    "type": "string",
    "regex": '^(?:(?:[\w`~!#$%^&*\-=+;:{}\'|,?\/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}\'|,?\/]+))*\.[\w`~!#$%^&*\-=+;:{}\'|,?\/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d\-]+(?:\.[a-zA-Z\d\-]+)*|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])$',  # noqa
}
_share_location = {
    "nullable": True,
    "type": "boolean"
}
_coord_lat = {
    "nullable": True,
    "type": "string",
    "regex": "^(-)?(?=.*[0-9]).{1,3}\.(?=.*[0-9]).{6,64}$",  # noqa
}
_coord_long = {
    "nullable": True,
    "type": "string",
    "regex": "^(-)?(?=.*[0-9]).{1,3}\.(?=.*[0-9]).{6,64}$",  # noqa
}


# ** «««««««««««««««« Validations »»»»»»»»»»»»»»»» **


def _on_post(request):
    doc = {
        "password": request.json.get("password"),
        "firstName": request.json.get("firstName"),
        "lastName": request.json.get("lastName"),
        "email": request.json.get("email"),
        "shareLocation": request.json.get("shareLocation"),
        "coordLat": str(request.json.get("coordLat")),
        "coordLong": str(request.json.get("coordLong")),
    }
    schema = {
        "password": {**_password, **_required},
        "firstName": {**_first_name, **_required},
        "lastName": {**_last_name, **_required},
        "email": {**_email, **_required},
        "shareLocation": {**_share_location, **_required},
        "coordLat": {**_coord_lat, **_required},
        "coordLong": {**_coord_long, **_required},
    }

    # Run validation
    validator(request, schema, doc)


user_validate_on_post = RouteDecorator(req=_on_post)


def _on_patch(request):
    doc = {
        "password": request.json.get("password"),
        "firstName": request.json.get("firstName"),
        "lastName": request.json.get("lastName"),
        "email": request.json.get("email"),
        "shareLocation": request.json.get("shareLocation"),
    }
    if request.json.get("coordLat"):
        doc = {
            **doc,
            "coordLat": str(request.json.get("coordLat")),
        }
    if request.json.get("coordLong"):
        doc = {
            **doc,
            "coordLong": str(request.json.get("coordLong")),
        }
    schema = {
        "password": _password,
        "firstName": _first_name,
        "lastName": _last_name,
        "email": _email,
        "shareLocation": _share_location,
        "coordLat": _coord_lat,
        "coordLong": _coord_long,
    }

    # Run validation
    validator(request, schema, doc)


user_validate_on_patch = RouteDecorator(req=_on_patch)
