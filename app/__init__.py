from flask import Flask, session, g, render_template
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

    # Before each request, inject
    # the user object into the global flask 
    # 'g' object so that we can pass it down
    # to every template.
    @app.before_request
    def load_user():
        token = session.get("token")
        account = None

        if token:
            try:
                token_payload = jwt.decode(token, app.config['SECRET_KEY'])
                account = Account.query.filter_by(id = token_payload['id']).first()
            except:
                account = None
                session.pop("token")

        g.logged_in_user = account

    from .routes import routes
    from .authentication import auth

    app.register_blueprint(routes)
    app.register_blueprint(auth)

    def page_not_found(e):
        return render_template('404.html'), 404

    app.register_error_handler(404, page_not_found)

    return app