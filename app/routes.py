from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify
from .authentication import protected_view
from .models import *
from sqlalchemy import extract

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/dashboard")
@protected_view
def dashboard(current_user):
    return render_template("dashboard.html")

@routes.route("/browse")
def browse():
    return render_template("browse.html", genres=db.session.query(Genre).all())

@routes.route("/do-get-genres", methods=["GET"])
def do_get_genres():
    result = []
    for genre in db.session.query(Genre).all():
        result.append(genre.to_dict())

    return jsonify(result)

@routes.route("/do-get-movies-page", methods=["POST"])
def do_get_movies_page():
    result = []

    movies = db.session.query(Movie)
    genres = request.form.getlist("genres[]")
    if (len(genres) > 0):
        movies = movies.filter(Movie.genres.any(Genre.id.in_(request.form.getlist("genres[]"))))

    years = request.form.getlist("years[]")
    if (len(years) > 0):
        movies = movies.filter(extract("year", Movie.releaseDate).in_(request.form.getlist("years[]")))

    movies = movies.order_by(Movie.title.asc(), Movie.releaseDate.desc())\
                   .paginate(int(request.form["page"]), int(request.form["amount"]), False)\
                   .items

    for movie in movies:
        result.append(movie.to_dict())

    return jsonify({ "success": True, "movies": result })

@routes.route("/do-add-movie", methods=["POST"])
def do_add_movie():
    if db.session.query(Movie.id).filter_by(title=request.form["title"], releaseDate=request.form["release-date"]).scalar() is not None:
        return jsonify({"success": False, "reason": "movie exists"})

    movie = Movie(\
        title = request.form["title"],\
        releaseDate = request.form["release-date"],\
        thumbnailSrc = "static/images/image.png",\
        runtime = request.form["runtime"],\
        maturity_rating = request.form["maturity-rating"] #assumes the client has gotten list of maturity ratings
    )

    for id in request.form.getlist("genres[]"):
        genre = db.session.query(Genre).filter_by(id=id).one()
        movie.genres.append(genre)

    db.session.add(movie)
    db.session.commit()

    return jsonify({ "success": True })
