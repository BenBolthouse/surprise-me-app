from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_socketio import emit
from socketio.exceptions import SocketIOError
from sqlalchemy import and_, desc, or_
from werkzeug.exceptions import BadRequest, Forbidden

from app import socketio
from models import db, Connection, Message


message_routes = Blueprint("message_routes", __name__, url_prefix="/api/v1/connections")


# POST https://surprise-me.benbolt.house/api/v1/connections/<connection_id>/messages
# Creates a new message for the given connection and handles emitting the
# message to connected parties.
@message_routes.route("/<connection_id>/messages", methods=["POST"])
def post(connection_id):
    get = request.json.get

    body = get("body")

    connection = Connection.query.filter(
        and_(
            or_(
                Connection._requestor_id == current_user.id,
                Connection._approver_id == current_user.id),
            Connection._id == int(connection_id))).first()

    # handle bad requests for non-member users
    if not connection:
        raise BadRequest(response={
            "message": "User not connected to recipient user",
        })

    other_user = connection.other_user(current_user.id)
    recipient_id = other_user["id"]

    message_room_name = f"message_room_{recipient_id}"

    message = Message(int(connection_id), current_user.id, recipient_id, body)

    db.session.add(message)
    db.session.commit()

    response = {
        "message": "Success",
        "data": {
            "connection_id": int(connection_id),
            "messages": [message.to_dict()],
        }
    }

    # emit to user's message room
    socketio.emit("deliver_message", response, to=message_room_name)

    return jsonify(response), 201


# GET https://surprise-me.benbolt.house/api/v1/connections/<connection_id>/messages
# Retrieves a set and offset quantity of messages based on url queries.
@ message_routes.route("/<connection_id>/messages", methods=["GET"])
@ login_required
def get(connection_id):
    offset = request.args.get("ofs")
    limit = request.args.get("lim")

    # handle bad requests for poorly-formatted requests
    if not offset or not limit:
        raise BadRequest(response={
            "message": "Missing request args"
        })

    connection = Connection.query.filter(
        and_(
            or_(
                Connection._requestor_id == current_user.id,
                Connection._approver_id == current_user.id),
            Connection._id == int(connection_id))).first()

    # handle bad requests for non-member users
    if not connection:
        raise Forbidden(response={
            "message": "User not member",
        })

    # get offset limit of messages and format for json response
    messages = Message.query.filter(Message._connection_id == int(connection_id))\
        .order_by(Message._id.desc())\
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
