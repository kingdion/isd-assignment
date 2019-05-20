from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:isd_password@localhost:5432/isd",
    SQLALCHEMY_TRACK_MODIFICATIONS = True,
    SECRET_KEY = "Change in production",
    DEBUG = True,
)

db = SQLAlchemy(app)

from .routes import routes

app.register_blueprint(routes)