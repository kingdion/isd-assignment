import jwt
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app, session
from functools import partial
from .authentication import protected_view
from .models import *
from sqlalchemy import extract

routes = Blueprint("routes", __name__)

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

# protected_view_staff = partial(protected_view, staff_required=True)
# @routes.route("/browse-modify")
# @protected_view_staff
# def browse_modify():
#     return render_template("browse-modify.html", genres=db.session.query(Genre).all())

@routes.route("/profile")
@protected_view
def profile():
    return render_template("profile.html")

@routes.route("/logs")
@protected_view
def logs():
    return render_template("logs.html")

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

    years = request.form.getlist("years[]")
    if (len(years) > 0):
        movies = movies.filter(extract("year", Movie.release_date).in_(request.form.getlist("years[]")))

    movies = movies.order_by(Movie.title.asc(), Movie.release_date.desc())\
                   .paginate(int(request.form["page"]), int(request.form["amount"]), False)\
                   .items

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

    for movie in movies:
        result += '<div class="movie-cell" id="' + str(movie.id) + '"><img src="' + movie.thumbnail_src + '" alt="' + movie.title + '">'
        if (isStaff):
            result += '<div class="movie-buttons">\
                         <button type="button" class="btn btn-dark edit-movie-btn" data-toggle="tooltip" data-placement="top" title="Edit movie details">\
                           <i class="far fa-edit"></i>\
                         </button>\
                         <div class="spacer-h"></div>\
                         <button type="button" class="btn btn-dark add-copy-btn" data-toggle="tooltip" data-placement="top" title="Add a copy of this movie">\
                            <i class="fas fa-compact-disc"></i>\
                         </button>\
                         <div class="spacer-h"></div>\
                         <button type="button" class="btn btn-dark delete-movie-btn" data-toggle="tooltip" data-placement="top" title="Delete this movie">\
                            <i class="far fa-trash-alt"></i>\
                         </button>\
                       </div>'
        result += '<div class="movie-description">' + movie.title + '<br>(' + str(movie.release_date.year) + ')</div></div>'

    return jsonify({ "success": True, "gridHtml": result + "</div>" })

@routes.route("/add-movie")
@protected_view
def add_movie():
    return render_template("add_movie.html")

@routes.route("/do-add-movie", methods=["POST"])
def do_add_movie():
    if db.session.query(Movie.id).filter_by(title=request.form["title"], release_date=request.form["release-date"]).scalar() is not None:
        return jsonify({"success": False, "reason": "movie exists"})

    movie = Movie(\
        title = request.form["title"],\
        release_date = request.form["release-date"],\
        thumbnail_src = "static/images/image.png",\
        runtime = request.form["runtime"],\
        maturity_rating = request.form["maturity-rating"] #assumes the client has gotten list of maturity ratings
    )

    for id in request.form.getlist("genres[]"):
        genre = db.session.query(Genre).filter_by(id=id).one()
        movie.genres.append(genre)

    db.session.add(movie)
    db.session.commit()

    return jsonify({ "success": True })

@routes.route("/edit-movie/<movieID>")
@protected_view
def edit_movie(movieID):
    try:
        movie = Movie.query.filter_by(id=movieID).one()
        return render_template("edit_movie.html", movie=movie)
    except:
        return 'Something went wrong trying to edit this movie.', 400
