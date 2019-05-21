import uuid
import jwt
import datetime
from flask import Flask, request, session, jsonify, make_response, Blueprint, \
                render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from . import app, db
from .models import *

auth = Blueprint("auth", __name__)

''' 
Decorator to protect a view, wraps around a view function 
and checks the request header for x-access-token, if one is 
given and is valid, the view will be returned and the view function
will have access to a logged in user.
'''
def protected_view(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("token")

        if token == None:
            return redirect(url_for('auth.login_page'))

        try: 
            token_payload = jwt.decode(token, app.config['SECRET_KEY'])
            account = Account.query.filter_by(id = token_payload['id']).first()
        except:
            return redirect(url_for('auth.login_page'))

        return f(account, *args, **kwargs)
    return decorated

@auth.route("/login")
def login_page():
    return render_template("login.html")

@auth.route("/do-login", methods=["POST"])
def do_login():
    username = request.form.get("email")
    password = request.form.get("password")

    if not username and not password:
        return jsonify({'message' : 'Invalid login request data'}), 401

    return login(username, password)

def login(username, password):
    login_token = get_login_token(username, password)

    if login_token == None:
        return jsonify({'message' : 'Invalid credentials'}), 401

    session["token"] = login_token.decode('UTF-8')

    return jsonify({'token' : login_token.decode('UTF-8')})

def get_login_token(username, password):
    account = Account.query.filter_by(email = username).first()

    if not account:
        return None

    if check_password_hash(account.password, password):
        token = jwt.encode({'id' : str(account.id), 
                            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, # expires in 60 minutes
                            app.config['SECRET_KEY'])
        return token

    return None

@auth.route("/logout")
def logout():
    session["token"] = None
    return "success"

@auth.route("/register")
def register():
    return render_template("register.html")

@auth.route("/do-register", methods=["POST"])
def do_register():
    email_exists = db.session.query(Account.email).filter_by(email=request.form["email"]).scalar() is not None

    if email_exists:
        return jsonify({"success": False, "reason": "email exists"})

    account = Account(\
        first_name=request.form["first-name"],\
        last_name=request.form["last-name"],\
        email=request.form["email"],\
        password=generate_password_hash(request.form["password"], method='sha256'),\
        street_address=request.form["street-address"],\
        postcode=request.form["postcode"],\
        is_staff=False\
    )

    # TODO: Add server-side validation (since clients can just alter the javascript to bypass client-side validation)

    db.session.add(account)
    db.session.commit()

    return login(request.form["email"], request.form["password"])