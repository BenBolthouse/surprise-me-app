from flask import Blueprint, jsonify
from flask_socketio import send
from traceback import format_exc, format_tb, format_stack
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from werkzeug.exceptions import InternalServerError, Unauthorized


from app import app, socketio


error_routes = Blueprint("errors_routes", __name__)


# Handle 400 range API errors.
@app.errorhandler(BadRequest)
@app.errorhandler(NotFound)
@app.errorhandler(Forbidden)
@app.errorhandler(Unauthorized)
@app.errorhandler(InternalServerError)
def handle_werkzeug_exceptions(exception):
    return jsonify(exception.response), exception.code


# Handle 500 range errors and raised exceptions.
@app.errorhandler(Exception)
def handle_all_other_exceptions(exception):
    return jsonify({
        "notification": {
            "body": "An error ocurred. Please refresh your browser and try again. If this issue persists then contact us.",
            "type": "card_notifications",
        },
    }), 500


# Captures all error events and sends them back to the client.
@socketio.on_error_default
def event_error_default(error):
    send(error.args[0])
