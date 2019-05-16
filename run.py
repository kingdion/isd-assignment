import os
import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.models import Movie, Genre, MovieGenre, Account, MovieOrderLine, Orders
from app import app, db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/do-login")
def do_login():
    return redirect(url_for('dashboard'))

def do_login_manual(username, password):
    pass

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/do-register", methods=["POST"])
def do_register():
    email_exists = db.session.query(Account.email).filter_by(email=request.form["email"]).scalar() is not None

    if email_exists:
        return jsonify({"success": False, "reason": "email exists"})

    account = Account(\
        first_name=request.form["first-name"],\
        last_name=request.form["last-name"],\
        email=request.form["email"],\
        password=request.form["password"],\
        street_address=request.form["street-address"],\
        postcode=request.form["postcode"],\
        is_staff=False\
    )

    # TODO: Add server-side validation (since clients can just alter the javascript to bypass client-side validation)

    db.session.add(account)
    db.session.commit()

    # TODO: Return login() or whatever, Dion will implement later
    return jsonify({"success": True})

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/browse")
def browse():
    return render_template("browse.html")

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
