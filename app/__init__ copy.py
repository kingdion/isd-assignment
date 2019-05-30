from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .routes import routes

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/isd",
    SQLALCHEMY_TRACK_MODIFICATIONS = True,
    SECRET_KEY = "Change in production",
    DEBUG = True,
)

db = SQLAlchemy(app)

app.register_blueprint(routes)