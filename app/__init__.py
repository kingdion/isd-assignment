from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
debugMode = True

if debugMode:
    app.config.update(
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:isd_password@localhost:5432/isd",
        SQLALCHEMY_TRACK_MODIFICATIONS = True, 
        SECRET_KEY = "Change in production",
        SESSION_COOKIE_SECURE = False,
        DEBUG = True,
    )
else:
    app.config.update(
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:isd_password@localhost:5432/isd",
        SQLALCHEMY_TRACK_MODIFICATIONS = False, 
        SECRET_KEY = "C94222125//34/rtgtrwrubwui24984524nfejsrjbf5", # randomly generated string
        SESSION_COOKIE_SECURE = True,
        DEBUG = False,
    )

db = SQLAlchemy(app)

from .routes import routes
from .authentication import auth

app.register_blueprint(routes)
app.register_blueprint(auth)