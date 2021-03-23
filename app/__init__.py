from flask import Flask, session, request, redirect, jsonify
from flask import send_from_directory
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import validate_csrf
from seed import seed_commands
from flask_socketio import SocketIO, emit
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from werkzeug.exceptions import InternalServerError, Unauthorized
import os
import traceback


from config import Config
from models import db, User


# Route imports
from routes import chat_message_routes
from routes import csrf_routes
from routes import s3_routes
from routes import session_routes
from routes import user_connection_routes
from routes import user_routes

is_prod = os.environ.get("FLASK_ENV") == "production"

# Development static app location
static_folder = "static/" if is_prod else "../react/build/"

app = Flask(__name__, static_folder=static_folder)

# Configure websockets
socketio = SocketIO(app,
                    logger=True,
                    engineio_logger=True,
                    cors_allowed_origins="*")

# Environment setup
app.config.from_object(Config)

# User login configuration
login = LoginManager(app)


@login.user_loader
def load_session_user(id):
    return User.query.get(int(id))


# Provide a command to seed the database
app.cli.add_command(seed_commands)


# Require a valid X-CSRFToken for all state-changing requests
@app.before_request
def validate_csrf_token():
    is_post = request.method == "POST"
    is_patch = request.method == "PATCH"
    is_delete = request.method == "DELETE"
    if is_post or is_patch or is_delete:
        print("")
        csrf_token = request.headers.get("X-CSRFToken")
        validate_csrf(csrf_token)


# Route configuration
app.register_blueprint(chat_message_routes)
app.register_blueprint(csrf_routes)
app.register_blueprint(s3_routes)
app.register_blueprint(session_routes)
app.register_blueprint(user_connection_routes)
app.register_blueprint(user_routes)

# Configure socketio events
from events import events  # noqa

# Models and migration configuration
db.init_app(app)
Migrate(app, db)

# Security configuration
CORS(app)


@app.before_request
# Redirect to HTTPS if in production
def https_redirect():
    if is_prod:
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


@app.errorhandler(InternalServerError)
@app.errorhandler(BadRequest)
@app.errorhandler(NotFound)
@app.errorhandler(Forbidden)
@app.errorhandler(Unauthorized)
# Sends responses automatically from
# raised exceptions in http routes
def handle_werkzeug_exceptions(exception):
    return jsonify(exception.response), exception.code


@app.errorhandler(Exception)
# Sends responses for all other raise
# exceptions
def handle_all_other_exceptions(exception):
    trace = exception.with_traceback(exception.__traceback__)
    trace_array = [t for t in trace.args]
    return jsonify({
        "message": "There was an unexpected internal server error.",
        "traceback": trace_array
    }), 500


if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=os.environ.get("PORT"),
        debug=False)
