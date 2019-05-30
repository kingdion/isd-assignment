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

# Decorator to protect a view, wraps around a view function
# and checks the request header for x-access-token, if one is
# given and is valid, the view will be returned and the view function
# will have access to a logged in user.

def protected_view(f, staff_required=False):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("token")

        # If no token, we don't have a user
        
        if token == None:
            return redirect(url_for('auth.login_page'))

        try:
            token_payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            account = Account.query.filter_by(id = token_payload['id']).first()

            # If there's a valid token but no account (say it was a deleted account and token still exists)
            # then we redirect to login.

            if account == None:
                return redirect(url_for('auth.login_page'))

            if (account and staff_required and not account.is_staff):
                return "Only staff members can view this page.", 403
        except:
            # If we fail to decode the token and find a user 
            # we need the user to login

            return redirect(url_for('auth.login_page'))

        # return function that we are wrapping

        return f(*args, **kwargs)
    return decorated

'''

User Registration

'''

@auth.route("/register", methods=["GET"])
def register():
    # Get the register form page 

    return render_template("register.html")

@auth.route("/do-register", methods=["POST"])
def do_register():
    # Submit the register request from the form
    # Perform server-side validation and then create the account
    # and add it to the database (then log the user in with it)

    account_exists = db.session.query(Account).filter((Account.email==request.form["email"]) | (Account.username==request.form["username"])).first()
        
    if account_exists:
        return jsonify({"success": False, "reason": "email exists"})

    keys = ["first-name", "last-name", "email", "username", "password", "street-address", "postcode", "phone-number"]

    empty_validation = validate_not_empty(request, keys)
    if (empty_validation != None):
        return empty_validation

    username = request.form["username"]
    password = request.form["password"]

    # TODO: Add server-side validation (since clients can just alter the javascript to bypass client-side validation)

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

    value = ""
    if request.method =='POST':
        value = request.form.get('isStaff')
        if value == "Staff":
            value = True
        else:
            value = False
    
    account = Account(\
        first_name=request.form["first-name"],\
        last_name=request.form["last-name"],\
        email=request.form["email"],\
        username=username,\
        password=generate_password_hash(password, method='sha256'),\
        street_address=request.form["street-address"],\
        postcode=request.form["postcode"],\
        phone_number=request.form["phone-number"],\
        is_staff=value,\
        is_active=True,\
        join_date=datetime.datetime.utcnow()\
    )

    db.session.add(account)
    db.session.commit()

    return jsonify({"success": True})

@auth.route("/update-registration-details", methods=["POST", "PUT"])
@protected_view
def update_registration_details():
    try:
        # Try access the global logged in user and update it
        # according to the users' changes. Verify no data is empty.
        keys = ["first_name", "last_name", "postcode", "phone_number", "street_address"]

        empty_validation = validate_not_empty(request, keys)
        if (empty_validation != None):
            return empty_validation

        g.logged_in_user.first_name = request.form["first_name"]
        g.logged_in_user.last_name = request.form["last_name"]
        g.logged_in_user.postcode = request.form["postcode"]
        g.logged_in_user.phone_number = request.form["phone_number"]
        g.logged_in_user.street_address = request.form["street_address"]

        db.session.commit()
    except:
        return jsonify({"success": False, "message": "Something went wrong trying to save your changes."})

    return jsonify({"success": True, "message": "Your details have been successfully changed!"})

def validate_not_empty(request, keys):
    for key in keys:
        if not request.form[key]:
            return jsonify({"success": False, "message": f"{key.replace('_', ' ').capitalize()} cannot be empty."}) 

@auth.route("/delete-account", methods=["POST", "DELETE"])
@protected_view
def delete_account():
    # Remove and logout the user from the session,
    # return a success response.

    db.session.delete(g.logged_in_user)
    session.pop('token', None)
    db.session.commit()

    return jsonify({"success": True, "message": "Your account has been successfully deleted"})

'''

User Login

'''

@auth.route("/login")
def login_page():
    # First check if the user is logged in
    # and return them to the dashboard 
    # if they are already logged in

    token = session.get("token")
    if token:
        token_payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        account = Account.query.filter_by(id = token_payload['id']).first()

        if account != None:
            return redirect(url_for("routes.browse"))

    return render_template("login.html")

@auth.route("/do-login", methods=["POST"])
def do_login():
    # Get data from the form input, check if they are valid
    # and send login data to the login function

    keys = ["username", "password"]

    empty_validation = validate_not_empty(request, keys)
    if (empty_validation != None):
        return empty_validation

    username = request.form.get("username")
    password = request.form.get("password")

    login_attempt = login(username, password)

    # On success, we send the user to the dashboard
    # otherwise just ask them to login again.

    return login_attempt

def login(username, password):
    # See if a login is successful and return
    # a valid JSON response
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

        # Create a new JWT token
        token = jwt.encode({'id' : str(account.id),
                            'exp' : now + datetime.timedelta(minutes=60)}, # expires in 60 minutes
                            current_app.config['SECRET_KEY'])

        # Add access log
        log = UserAccessLog(account.id, now, AccessLogTypes.login.value)
        db.session.add(log)
        db.session.commit()

        return token

    return None

@auth.route("/delete-log", methods=["POST", "DELETE"])
@protected_view
def delete_log():
    # On a delete log request,
    # remove the log from the database
    # and return a message so that javascript knows what
    # to remove.

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

# An enumeration of the different types of logs we can have
class AccessLogTypes(Enum):
    login = "Login"
    logout = "Logout"
