from flask import Flask, session, request, redirect, jsonify
from flask import send_from_directory
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
from flask_wtf.csrf import validate_csrf
from seed import seed_commands
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from werkzeug.exceptions import InternalServerError, Unauthorized
import os
import traceback


from config import Config
from models import db, User


app = Flask(__name__, static_folder="static/")

app.config.from_object(Config)

socketio = SocketIO(
    app,
    logger=True,
    engineio_logger=True,
    cors_allowed_origins="*"
)

# blueprints
from events import error_events
from events import message_events
from events import notification_events
from events import socket_connection_events
from routes import connection_routes
from routes import csrf_routes
from routes import file_routes
from routes import session_routes
from routes import user_routes
app.register_blueprint(error_events)
app.register_blueprint(message_events)
app.register_blueprint(notification_events)
app.register_blueprint(socket_connection_events)
app.register_blueprint(connection_routes)
app.register_blueprint(csrf_routes)
app.register_blueprint(file_routes)
app.register_blueprint(session_routes)
app.register_blueprint(user_routes)

login_manager = LoginManager(app)

# configure seed data cli
app.cli.add_command(seed_commands)


db.init_app(app)
migrate = Migrate(app, db)

cors = CORS(app)


# require a valid CSRF token for all state-changing http requests
@app.before_request
def validate_csrf_token():
    post = request.method == "POST"
    patch = request.method == "PATCH"
    delete = request.method == "DELETE"
    if post or patch or delete:
        print("")
        csrf_token = request.headers.get("X-CSRFToken")
        validate_csrf(csrf_token)


# configure the session user
@login_manager.user_loader
def load_session_user(id):
    return User.query.get(int(id))


# redirect to https if in production
@app.before_request
def https_redirect():
    if Config.IS_PRODUCTION_ENV:
        if request.headers.get("X-Forwarded-Proto") == "http":
            url = request.url.replace("http://", "https://", 1)
            code = 301
            return redirect(url, code=code)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


# handle 400 range API errors
@app.errorhandler(BadRequest)
@app.errorhandler(NotFound)
@app.errorhandler(Forbidden)
@app.errorhandler(Unauthorized)
def handle_werkzeug_exceptions(exception):
    return jsonify(exception.response), exception.code


# handle 500 range errors and raised exceptions
@app.errorhandler(InternalServerError)
@app.errorhandler(Exception)
def handle_all_other_exceptions(exception):
    trace = exception.with_traceback(exception.__traceback__)
    trace_array = [t for t in trace.args]
    return jsonify({
        "message": "There was an unexpected internal server error.",
        "traceback": trace_array,
    }), 500


# run flask webserver via socketio (development only)
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=os.environ.get("PORT"), debug=False)
