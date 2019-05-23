from flask import Flask, session, g
import jwt

def create_app(debugMode = True):
    app = Flask(__name__)

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

    from .models import db, Account
    db.init_app(app)

    @app.before_request
    def load_user():
        token = session.get("token")
        account = None

        if token:
            token_payload = jwt.decode(token, app.config['SECRET_KEY'])
            account = Account.query.filter_by(id = token_payload['id']).first()

        g.logged_in_user = account

    @app.context_processor
    def context_processor():
        return dict(logged_in_user={"username":"penis"})

    from .routes import routes
    from .authentication import auth

    app.register_blueprint(routes)
    app.register_blueprint(auth)

    return app