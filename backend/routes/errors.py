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
def handle_werkzeug_exceptions(exception):
    return jsonify(exception.response), exception.code


# Handle 500 range errors and raised exceptions.
@app.errorhandler(InternalServerError)
@app.errorhandler(Exception)
def handle_all_other_exceptions(exception):
    return jsonify({
        "message": "There was an unexpected internal server error",
        "data": {
            "details": exception.name,
            "traceback": format_stack(),
        },
    }), 500


# Captures all error events and sends them back to the client.
@socketio.on_error_default
def event_error_default(error):
    send(error.args[0])
