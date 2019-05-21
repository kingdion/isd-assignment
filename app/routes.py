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
    genres = request.form.getlist("genres[]")
    years = request.form.getlist("years[]")
    ratings = request.form.getlist("ratings[]")
    index = request.form["index"]
    length = request.form["amount"]

    movies = db.session.query(Movie)
    print(movies) #use sql alchemy slice

    return jsonify({"success": False})

@routes.route("/do-add-movie")
def do_add_movie():
    movie_exists = False #later this will actually check

    if movie_exists:
        return jsonify({"success": False, "reason": "movie exists"})

    movie = Movie(\
        title = request.form["title"],\
        releaseDate = request.form["release-date"],\
        thumbnailSrc = "static/images/image.png",\
        runtime = request.form["runtime"],\
        maturity_rating = int(request.form["maturity-rating"]) #assumes the client has gotten list of maturity ratings
        #genre? not sure how alchemy works with associative entities, should ask dion
    )

    for genre in request.form.getlist("genres[]"):
        email_exists = db.session.query(Account.email).filter_by(email=request.form["email"]).scalar() is not None
        dbGenreID = db.session.query(Genre).filter_by(name=genre).one()
        movie.genres.append(dbGenreID)

    db.session.add(movie)
    db.session.commit()

    return jsonify({"success": True})

@routes.route("/do-get-genres", methods=["GET"])
def do_get_genres():
    result = []
    genres = db.session.query(Genre).all()
    for genre in genres:
        result.append(genre.__dict__)

    return jsonify(result)
