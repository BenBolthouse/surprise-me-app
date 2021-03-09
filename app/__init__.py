from flask import Flask, session, request, redirect, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import validate_csrf
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
import os
import traceback

from config import Config
from models import db, User


# Route imports
from routes import csrf_routes
from routes import s3_routes
from routes import session_routes
from routes import user_connection_routes
from routes import user_routes

app = Flask(__name__)

# Environment setup
app.config.from_object(Config)
is_production = os.environ.get('FLASK_ENV') == 'production'

# User login configuration
login = LoginManager(app)
login.login_view = 'auth.unauthorized'


@login.user_loader
def load_session_user(id):
    return User.get_by_id_on_session_user_load(int(id))


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
app.register_blueprint(csrf_routes)
app.register_blueprint(s3_routes)
app.register_blueprint(session_routes)
app.register_blueprint(user_connection_routes)
app.register_blueprint(user_routes)

# Models and migration configuration
db.init_app(app)
Migrate(app, db)

# Security configuration
CORS(app)


@app.before_request
# Redirect to HTTPS if in production
def https_redirect():
    if is_production:
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)


@app.route('/', defaults={'path': ''}, methods=["GET"])
@app.route('/<path:path>', methods=["GET"])
# Response with frontend
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


@app.errorhandler(InternalServerError)
@app.errorhandler(BadRequest)
@app.errorhandler(NotFound)
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
        "traceback": trace_array if not is_production else ""
    }), 500
