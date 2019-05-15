import os
import datetime
from flask import render_template, flash, redirect, url_for, request
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

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/do-register", methods=["POST"])
def do_register():
    account = Account(\
        first_name=request.form["first-name"],\
        last_name=request.form["last-name"],\
        email=request.form["email"],\
        password=request.form["password"],\
        street_address=request.form["street-address"],\
        postcode=request.form["postcode"],\
        is_staff=False\
    )

    db.session.add(account)
    db.session.commit()

    return redirect(url_for('dashboard'))

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
