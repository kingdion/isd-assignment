import jwt
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app, session
from functools import partial
from .authentication import protected_view
from .models import *
from sqlalchemy import extract
from operator import itemgetter
from werkzeug.utils import secure_filename

routes = Blueprint("routes", __name__)

protected_view_staff = partial(protected_view, staff_required=True)

@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/dashboard")
@protected_view
def dashboard():
    return render_template("dashboard.html")

@routes.route("/browse")
def browse():
    return render_template("browse.html", genres=db.session.query(Genre).all())

@routes.route("/profile")
@protected_view
def profile():
    return render_template("profile.html")

@routes.route("/logs")
@protected_view
def logs():
    return render_template("logs.html")

@routes.route("/payment")
@protected_view
def payment():
    return render_template("paymente.html")

@routes.route("/do-get-genres", methods=["GET"])
def do_get_genres():
    result = []
    for genre in db.session.query(Genre).all():
        result.append(genre.to_dict())

    return jsonify(result)

@routes.route("/do-get-movies-grid-html", methods=["POST"])
def do_get_movies_grid_html():

    movies = db.session.query(Movie)

    genres = request.form.getlist("genres[]")
    if (len(genres) > 0):
        movies = movies.filter(Movie.genres.any(Genre.id.in_(request.form.getlist("genres[]"))))

    movies = movies.order_by(Movie.title.asc(), Movie.release_date.desc()).all()

    scoredMovies = []
    searchString = request.form.get("title")
    for movie in movies:
        if searchString:
            score = score_movie_title(movie.title, searchString)
            if (score > 0):
                scoredMovies.append((movie, score, movie.title))
        else:
            scoredMovies.append((movie, 1, movie.title))

    if searchString:
        scoredMovies.sort(key=itemgetter(2))
        scoredMovies.sort(key=itemgetter(1), reverse=True)

    result = '<div class="movie-grid">'
    isStaff = False;
    token = session.get("token")
    if token != None:
        token_payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        isStaff = Account.query.filter_by(id = token_payload['id']).first().is_staff

    if (isStaff):
        result += '<div class="movie-cell">\
                     <a href="/add-movie">\
                       <div class="new-movie-placeholder">\
                         <i class="far fa-plus-square"></i>\
                       </div>\
                     </a>\
                   </div>'

    startIndex = int(request.form["page"]) * int(request.form["amount"])
    endIndex = startIndex + int(request.form["amount"])
    for movie, score, title in scoredMovies[startIndex : endIndex]:
        result += '<div class="movie-cell" id="' + str(movie.id) + '"><img src="' + movie.thumbnail_src + '" alt="' + movie.title + '">'
        if (isStaff):
            result += '<div class="movie-buttons">\
                         <button type="button" class="btn btn-dark edit-movie-btn" data-toggle="tooltip" data-placement="top" title="Edit movie details">\
                           <i class="far fa-edit"></i>\
                         </button>\
                         <div class="spacer-h"></div>\
                         <button type="button" class="btn btn-dark edit-movie-copies-btn" data-toggle="tooltip" data-placement="top" title="Edit copies of this movie">\
                            <i class="fas fa-compact-disc"></i>\
                         </button>\
                         <div class="spacer-h"></div>\
                         <button type="button" class="btn btn-dark delete-movie-btn" data-toggle="tooltip" data-placement="top" title="Delete this movie">\
                            <i class="far fa-trash-alt"></i>\
                         </button>\
                       </div>'
        result += '<div class="movie-description">' + movie.title + '<br>(' + str(movie.release_date.year) + ')</div></div>'

    return jsonify({ "success": True, "gridHtml": result + "</div>" })

def score_movie_title(title, searchTitle):
    if title == searchTitle:
        return 1

    searchWords = set(searchTitle.split());
    titleWords = set(title.split());

    score = 0;

    for searchWord in searchWords:
        for titleWord in titleWords:
            sWord = searchWord.lower()
            tWord = titleWord.lower()
            if sWord == tWord:
                score += 1
            elif (sWord in tWord and len(sWord) > 2) or (tWord in sWord and len(tWord) > 2):
                score += 0.5

    score = score / max(len(titleWords), len(searchWords))

    return score if score < 1 else 0.99

@routes.route("/add-movie")
@protected_view_staff
def add_movie():
    return render_template("add_movie.html", genres=db.session.query(Genre).all(), maturityRatings=db.session.query(MaturityRating).all())

@routes.route("/do-add-movie", methods=["POST"])
@protected_view_staff
def do_add_movie():
    if db.session.query(Movie.id).filter_by(title=request.form["title"], release_date=request.form["release-date"]).scalar() is not None:
        return jsonify({"success": False, "reason": "movie exists"})

    movie = Movie(\
        title = request.form["title"],\
        release_date = request.form["release-date"],\
        thumbnail_src = "static/images/image.png",\
        runtime = request.form["runtime"],\
        maturity_rating = request.form["maturity-rating"]
    )

    for id in request.form.getlist("genres[]"):
        genre = db.session.query(Genre).filter_by(id=id).one()
        movie.genres.append(genre)

    db.session.add(movie)
    db.session.commit()

    return jsonify({ "success": True })

@routes.route("/edit-movie/<movieID>")
@protected_view_staff
def edit_movie(movieID):
    try:
        movie = Movie.query.filter_by(id=movieID).one()
        return render_template("edit_movie.html", movie=movie, genres=db.session.query(Genre).all(), maturityRatings=db.session.query(MaturityRating).all())
    except Exception as e:
        print(e)
        return 'Something went wrong trying to edit this movie.', 400

@routes.route("/do-edit-movie", methods=["POST"])
@protected_view_staff
def do_edit_movie():
    try:
        movie = Movie.query.filter_by(id=request.form["id"]).one()
        movie.title = request.form["title"]
        movie.release_date = request.form["release-date"]
        movie.runtime = request.form["runtime"]
        movie.maturity_rating = request.form["maturity-rating"]
        movie.genres = [];
        for id in request.form.getlist("genres[]"):
            genre = db.session.query(Genre).filter_by(id=id).one()
            movie.genres.append(genre)
        db.session.commit()

        return render_template("edit_movie.html", movie=movie, genres=db.session.query(Genre).all(), maturityRatings=db.session.query(MaturityRating).all())
    except Exception as e:
        print(e)
        return 'Something went wrong trying submit edits to this movie.', 400

@routes.route("/edit-movie-copies/<movieID>")
@protected_view_staff
def add_movie_copy(movieID):
    try:
        movie = Movie.query.filter_by(id=movieID).one()
        return render_template("edit_movie_copies.html", movie=movie)
    except:
        return 'Something went wrong trying to edit copies of this movie.', 400

@routes.route("/delete-movie", methods=["POST"])
@protected_view_staff
def delete_movie():
    try:
        movie = Movie.query.filter_by(id=request.form["id"]).one()
        db.session.delete(movie)
        db.session.commit()
        return jsonify( {"success": True} )
    except:
        return 'Something went wrong trying to delete this movie.', 400
