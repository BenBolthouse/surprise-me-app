from flask import Flask, session, request, redirect, jsonify
from flask import send_from_directory
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
from flask_wtf.csrf import validate_csrf
import os


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
from routes import connection_routes
from routes import csrf_routes
from routes import file_routes
from routes import message_routes
from routes import notification_routes
from routes import session_routes
from routes import user_routes
from routes import error_routes
from seed import cmd
app.register_blueprint(connection_routes)
app.register_blueprint(csrf_routes)
app.register_blueprint(file_routes)
app.register_blueprint(message_routes)
app.register_blueprint(notification_routes)
app.register_blueprint(session_routes)
app.register_blueprint(user_routes)
app.register_blueprint(error_routes)
app.register_blueprint(cmd)


login_manager = LoginManager(app)


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


# send static files and react entrypoint
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


# run flask webserver via socketio (development only)
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=os.environ.get("PORT"), debug=False)
