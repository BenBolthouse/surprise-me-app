from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy import desc, or_
from werkzeug.exceptions import BadRequest, Forbidden

from app import socketio
from models import db, Connection, Message


message_routes = Blueprint("message_routes", __name__, url_prefix="/api/v1/connections")


# GET https://surprise-me.benbolt.house/api/v1/connections/<connection_id>/messages
# Retrieves a set and offset quantity of messages based on url queries.
@message_routes.route("/<connection_id>/messages", methods=["GET"])
@login_required
def get(connection_id):
    offset = request.args.get("ofs")
    limit = request.args.get("lim")

    # handle bad requests for poorly-formatted requests
    if not offset or not limit:
        raise BadRequest(response={
            "message": "Missing request args"
        })

    connection = Connection.query.filter(
        or_(
            Connection._requestor_id == current_user.id,
            Connection._approver_id == current_user.id)).first()

    # handle bad requests for non-member users
    if not connection:
        raise Forbidden(response={
            "message": "User not member",
        })

    # get offset limit of messages and format for json response
    messages = Message.query.filter(Message._connection_id == int(connection_id))\
        .order_by(Message._created_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()

    messages = [x.to_dict() for x in messages]

    return jsonify({
        "message": "Success",
        "data": {
            "connection_id": int(connection_id),
            "messages": messages,
        }
    }), 200
