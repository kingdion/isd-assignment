from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify
from . import db
from .models import Movie, Genre, MovieGenre, Account, MovieOrderLine, Orders

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/login")
def login():
    return render_template("login.html")

@routes.route("/do-login")
def do_login():
    return redirect(url_for('routes.dashboard'))

def do_login_manual(username, password):
    pass

@routes.route("/register")
def register():
    return render_template("register.html")

@routes.route("/do-register", methods=["POST"])
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

@routes.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@routes.route("/browse")
def browse():
    return render_template("browse.html")

@routes.route("/do-get-movies", methods=["POST"])
def do_get_movies():
    genres = request.form.getlist('genres[]')
    years = request.form.getlist('years[]')
    ratings = request.form.getlist('ratings[]')
    print(genres, years, ratings, request.form["test"])
    return jsonify({"success": False})

@routes.route("/do-add-movie")
def do_add_movie():
    movie_exists = False #later this will actually check

    if (movie_exists):
        return jsonify({"success": False, "reason": "movie exists"})

    movie = Movie(\
        title = request.form["title"],\
        releaseDate = request.form["release-date"],\
        thumbnailSrc = "static/images/image.png",\
        runtime = request.form["runtime"],\
        maturity_rating = request.form["maturity-rating"]
        #genre? not sure how alchemy works with associative entities, should ask dion
    )

    db.session.add(movie)
    db.session.commit()

    return jsonify({"success": False})