from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify
from . import db
from .authentication import protected_view
from .models import Movie, Genre, MovieGenre, Account, MovieOrderLine, Orders

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/dashboard")
@protected_view
def dashboard(current_user):
    print(current_user)
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