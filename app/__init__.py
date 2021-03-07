from flask import Flask, session, request, redirect
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import validate_csrf
import os

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
    return User.query.get(int(id))


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
