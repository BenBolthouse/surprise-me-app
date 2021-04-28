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
    "type": "string",
    "regex": "^(-)?(?=.*[0-9]).{1,3}\.(?=.*[0-9]).{6,64}$",  # noqa
}


def _post(req):
    target = {
        "password": req.json.get("password"),
        "firstName": req.json.get("firstName"),
        "lastName": req.json.get("lastName"),
        "email": req.json.get("email"),
        "shareLocation": req.json.get("shareLocation"),
    }
    schema = {
        "password": {**password, **required},
        "firstName": {**name, **required},
        "lastName": {**name, **required},
        "email": {**email, **required},
        "shareLocation": {"type": "boolean", **required},
    }
    validator(request, schema, target)


def _patch(request):
    target = {
        "firstName": request.json.get("firstName"),
        "lastName": request.json.get("lastName"),
    }
    schema = {
        "firstName": name,
        "lastName": name,
    }
    validator(request, schema, target)


def _patch_password(request):
    target = {
        "password": request.json.get("password"),
    }
    schema = {
        "password": {**password, **required},
    }
    validator(request, schema, target)


def _patch_email(request):
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
