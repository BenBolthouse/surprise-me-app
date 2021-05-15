from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy import and_, desc


from models import db, Notification


notification_routes = Blueprint("notification_routes", __name__, url_prefix="/api/v1/notifications")


# POST https://surprise-me.benbolt.house/api/v1/notifications
# Creates a new notification for a user.
@notification_routes.route("", methods=["POST"])
@login_required
def post():
    raise Exception("Not implemented")


# GET https://surprise-me.benbolt.house/api/v1/notifications
# Retrieves all unseen and non-dismissed notifications for a user by type.
@notification_routes.route("/<type>", methods=["GET"])
@login_required
def get(type):
    notifications = Notification.query.filter(
        and_(
            Notification.recipient_id == current_user.id,
            Notification.type == f"{type}_notification",
            Notification.dismissed_at == None))\
        .order_by(Notification.created_at.desc())\
        .all()  # noqa

    notifications = [x.to_dict() for x in notifications]

    return jsonify({
        "data": notifications,
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/notifications/see
# Updates a collection of notification as seen.
@notification_routes.route("/see", methods=["PATCH"])
@login_required
def patch_see():
    get = request.json.get

    notifications = get("notifications")

    for x in notifications:
        notification = Notification.query.get(x)

        notification.set_seen_at()

    db.session.commit()

    notifications = [x.to_dict() for x in notifications]

    return jsonify({
        "data": notifications,
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/notifications/dismiss
# Updates a collection of notification as dismissed.
@notification_routes.route("/dismiss", methods=["PATCH"])
@login_required
def patch_dismiss():
    get = request.json.get

    notifications = get("notifications")

    for x in notifications:
        notification = Notification.query.get(x)

        notification.set_seen_at()
        notification.set_dismissed_at()

    db.session.commit()

    notifications = [x.to_dict() for x in notifications]

    return jsonify({
        "data": notifications,
    }), 200
