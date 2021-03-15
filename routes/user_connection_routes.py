from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from config import Config
from models import db, User, UserConnection
from models import UserNotification, ChatMessage


user_connection_routes = Blueprint(
    "connections",
    __name__,
    url_prefix="/api/connections")


@user_connection_routes.route("", methods=["POST"])
@login_required
def post_user_connection():

    # Data from request
    recipient_id = request.json.get("recipientUserId")

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Respond 400 if connection user nonexistent
    recipient_user = User.get_by_id(recipient_id)

    # Check if the users are already connected
    user.user_by_id_is_a_connection(recipient_id)

    # Define the new connection
    new_connection = UserConnection({
        "requestor_user_id": user.id,
        "recipient_user_id": recipient_id,
    })

    # Add connection to the session user
    user.connections = new_connection

    # Commit changes
    db.session.commit()

    # Create notifications for connection user
    new_notification = UserNotification(
        recipient_id,
        "USER_CONN_REQ",
        f"{Config.HOST_NAME}/api/connections/{new_connection.id}",
        f"{user.first_name} {user.last_name} sent you a friend request.")

    recipient_user.notifications = new_notification

    # Commit changes
    db.session.commit()

    # Respond 201 if successful
    return jsonify({
        "message": "Success",
        "data": new_connection.to_json()
    }), 201


@user_connection_routes.route("/", methods=["GET"])
@login_required
def get_all_user_connections():

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Format data for the response
    response_date = []
    if scope == "sent":
        response_data = [
            x.to_json()
            for x in user.connections
            if x.user_by_id_is_requestor(user.id)]
    elif scope == "received":
        response_data = [
            x.to_json_as_recipient()
            for x in user.connections
            if x.user_by_id_is_recipient(user.id)]

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": response_data
    }), 200


@user_connection_routes.route("/pending", methods=["GET"])
@login_required
def get_pending_user_connections():

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Format data for the response
    response_data = [x.to_json()
                     for x in user.connections
                     if x.established_at is None
                     and x.user_by_id_is_requestor(user.id)]

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": response_data
    }), 200


@user_connection_routes.route("/established", methods=["GET"])
@login_required
def get_established_user_connections():

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Format data for the response
    response_data = [x.to_json_on_get_in_consumer_context(user.id)
                     for x in user.connections
                     if x.established_at is not None
                     and x.user_by_id_is_associated(user.id)]
    for connection in response_data:
        connection["messages"] = sorted(
                connection["messages"],
                key=lambda e: e["createdAt"],
                reverse=False)

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": {
            "datestamp": str(datetime.now()),
            "connections": response_data,
        },
    }), 200


@user_connection_routes.route("/established", methods=["POST"])
@login_required
def update_established_user_connections():

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    response_data = []

    datestamp = request.json.get("datestamp")

    client_connections = request.json.get("connections")

    for client_connection in client_connections:
        connection = UserConnection.query.get(client_connection["id"])
        if len(connection.messages) > client_connection["messagesCount"]:

            # Add the connection to the response data
            resp_conn = connection.to_json_on_get_in_consumer_context(user.id)
            resp_conn["messages"] = sorted(
                resp_conn["messages"],
                key=lambda e: e["createdAt"],
                reverse=False)
            response_data.append(resp_conn)

    return jsonify({
        "message": "Success",
        "data": {
            "datestamp": str(datetime.now()),
            "connections": response_data,
        }
    }), 200


@user_connection_routes.route("/<id>/<directive>", methods=["PATCH"])
@login_required
def patch_fulfill_user_connection(id, directive):

    # Get the connection
    connection = UserConnection.get_by_id(int(id))

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Respond 400 if user not associated with connection
    # (prevents requestor from establishing own requested connections)
    connection.user_by_id_is_recipient(user.id)

    # Establish or delete connection
    establish = directive == "accept"
    if establish:
        connection.established_at = datetime.now()

        # Send the requestor a notification
        requestor_user = User.query.get(connection.requestor_user_id)
        notification = UserNotification(
            user.id,
            "USER_CONN_REQ_ESTABLISHED",
            None,
            f"{user.first_name} {user.last_name} accepted your friend request.")  # noqa
        requestor_user.notifications = notification

        # Commit changes
        db.session.commit()
    else:
        # Else delete the connection request
        db.session.delete(connection)
        db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": connection.to_json() if establish else "deleted"  # noqa
    }), 200
