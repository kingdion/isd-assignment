import uuid
import jwt
import datetime
from flask import Flask, request, session, jsonify, make_response, Blueprint, \
                render_template, flash, redirect, url_for, request, jsonify, current_app, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import *
from enum import Enum

auth = Blueprint("auth", __name__)

'''
Decorator to protect a view, wraps around a view function
and checks the request header for x-access-token, if one is
given and is valid, the view will be returned and the view function
will have access to a logged in user.
'''
def protected_view(f, staff_required=False):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("token")
        if token == None:
            return redirect(url_for('auth.login_page'))

        try:
            token_payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            account = Account.query.filter_by(id = token_payload['id']).first()
            if (staff_required and not account.is_staff):
                return "Only staff members can view this page.", 403
        except:
            return redirect(url_for('auth.login_page'))

        return f(*args, **kwargs)
    return decorated

'''

User Registration

'''

@auth.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@auth.route("/do-register", methods=["POST"])
def do_register():
    email_exists = db.session.query(Account.email).filter_by(email=request.form["email"]).scalar() is not None

    if email_exists:
        return jsonify({"success": False, "reason": "email exists"})

    username = request.form["username"]
    password = request.form["password"]

    account = Account(\
        first_name=request.form["first-name"],\
        last_name=request.form["last-name"],\
        email=request.form["email"],\
        username=username,\
        password=generate_password_hash(password, method='sha256'),\
        street_address=request.form["street-address"],\
        postcode=request.form["postcode"],\
        phone_number=request.form["phone-number"],\
        is_staff=False,\
        is_active=True,\
        join_date=datetime.datetime.utcnow()\
    )

    # TODO: Add server-side validation (since clients can just alter the javascript to bypass client-side validation)

    db.session.add(account)
    db.session.commit()

    return login(username, password)



@auth.route("/do-create-user", methods=["POST"])
def do_create_user():
    email_exists = db.session.query(Account.email).filter_by(email=request.form["email"]).scalar() is not None

    if email_exists:
        return jsonify({"success": False, "reason": "email exists"})

    username = request.form["username"]
    password = request.form["password"]

    account = Account(\
        first_name=request.form["first-name"],\
        last_name=request.form["last-name"],\
        email=request.form["email"],\
        username=username,\
        password=generate_password_hash(password, method='sha256'),\
        street_address=request.form["street-address"],\
        postcode=request.form["postcode"],\
        phone_number=request.form["phone-number"],\
        is_staff=False,\
        is_active=True,\
        join_date=datetime.datetime.utcnow()\
    )

    # TODO: Add server-side validation (since clients can just alter the javascript to bypass client-side validation)

    db.session.add(account)
    db.session.commit()

    return jsonify({"success": True})


@auth.route("/update-registration-details", methods=["POST", "PUT"])
@protected_view
def update_registration_details():
    try:
        # Try access the global logged in user and update it
        # according to the users' changes.

        g.logged_in_user.first_name = request.form["first_name"]
        g.logged_in_user.last_name = request.form["last_name"]
        g.logged_in_user.postcode = request.form["postcode"]
        g.logged_in_user.phone_number = request.form["phone_number"]
        g.logged_in_user.street_address = request.form["street_address"]

        db.session.commit()
    except:
        return jsonify({"success": False, "message": "Something went wrong trying to save your changes."})

    return jsonify({"success": True, "message": "Your details have been successfully changed!"})

@auth.route("/delete-account", methods=["POST", "DELETE"])
@protected_view
def delete_account():
    # Remove and logout the user from the session
    db.session.delete(g.logged_in_user)
    session.pop('token', None)
    db.session.commit()

    return jsonify({"success": True, "message": "Your account has been successfully deleted"})

'''

User Login

'''

@auth.route("/login")
def login_page():
    if session.get("token"):
        return redirect(url_for("routes.dashboard"))

    return render_template("login.html")

@auth.route("/do-login", methods=["POST"])
def do_login():
    # Get data from the form input, check if they are valid
    # and send login data to the login function

    username = request.form.get("username")
    password = request.form.get("password")

    login_attempt = login(username, password)

    if (login_attempt.get_json())["success"] == True:
        return redirect(url_for("routes.dashboard"))
    else:
        return redirect(url_for("auth.login_page"))

def login(username, password):
    # See if a login is successful and return
    # a valid JSON response
    if not username and not password:
        return jsonify({'success': False, 'message' : 'Invalid login request data'})

    login_token = get_login_token(username, password)

    if login_token == None:
        return jsonify({'success': False, 'message' : 'Invalid credentials'})

    session["token"] = login_token.decode('UTF-8')

    return jsonify({'success': True, 'token' : login_token.decode('UTF-8')})

def get_login_token(username, password):
    # Return a token if the user exists and
    # the password matches the user's password

    account = Account.query.filter_by(username = username).first()

    if not account:
        return None

    if check_password_hash(account.password, password):
        now = datetime.datetime.utcnow()
        token = jwt.encode({'id' : str(account.id),
                            'exp' : now + datetime.timedelta(minutes=60)}, # expires in 60 minutes
                            current_app.config['SECRET_KEY'])

        log = UserAccessLog(account.id, now, AccessLogTypes.login.value)
        db.session.add(log)
        db.session.commit()

        return token

    return None

@auth.route("/delete-log", methods=["POST", "DELETE"])
@protected_view
def delete_log():
    try:
        log = UserAccessLog.query.filter_by(id = request.form["log_id"]).first()
        db.session.delete(log)
        db.session.commit()
    except:
        return jsonify({'success': False, 'message' : 'Something went wrong trying to delete this log.'})

    return jsonify({'success': False, 'message' : 'The log has been deleted.'})

@auth.route("/logout")
@protected_view
def logout():
    # Since we validate our user based on the token
    # stored in the HTTPonly secure session cookie
    # All we do is remove it to log a user out
    log = UserAccessLog(g.logged_in_user.id, datetime.datetime.utcnow(), AccessLogTypes.logout.value)
    db.session.add(log)
    db.session.commit()

    session.pop('token', None)

    return redirect(url_for("routes.index"))

class AccessLogTypes(Enum):
    login = "Login"
    logout = "Logout"
