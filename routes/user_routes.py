from flask import Blueprint, request, jsonify


from models import db, User


from .user_routes_validation import user_validate_on_create

user_routes = Blueprint("users", __name__, url_prefix="/api/users")


@user_routes.route("", methods=["POST"])
@user_validate_on_create()
def create_new_user():

    # Respond 400 if body data validation failed
    body_data_validation_failed = request.validation_result is False
    if body_data_validation_failed:
        return jsonify({
            "message": "body_data_validation_failed",
            "data": request.validation_errors
        }), 400

    # Respond 400 if requested email is in use
    email = request.json["email"]
    requested_email_is_in_use = User.query.filter(
        User.email == email).first()
    if requested_email_is_in_use:
        return jsonify({
            "message": "requested_email_is_in_use",
            "data": {
                "details": f"The email {email} is already in use."
            }
        }), 400

    # Create the user and commit
    user = User({
        "password": request.json["password"],
        "first_name": request.json["firstName"],
        "last_name": request.json["lastName"],
        "email": request.json["email"],
        "share_location": request.json["shareLocation"],
        "coord_lat": request.json["coordLat"],
        "coord_long": request.json["coordLong"],
    })
    db.session.add(user)
    db.session.commit()

    # Respond 201 if successful
    return jsonify({
        "message": "success",
        "data": user.to_json_on_create()
    }), 201
