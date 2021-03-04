from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager


from config import Config
from models import db


# Route imports
from routes import user_routes

app = Flask(__name__)

# Environment setup
app.config.from_object(Config)

# User login configuration
login = LoginManager(app)
login.login_view = 'auth.unauthorized'


@login.user_loader
def load_session_user(id):
    # TODO add scoped user object to session
    pass


# Route configuration
app.register_blueprint(user_routes)

# Models and migration configuration
db.init_app(app)
Migrate(app, db)

# Security configuration
CORS(app)
