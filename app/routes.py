import jwt
import uuid
import math
import os
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app, session, g
from functools import partial
from .authentication import protected_view
from .models import *
from sqlalchemy import extract
from operator import itemgetter
from werkzeug.utils import secure_filename
from datetime import date


routes = Blueprint("routes", __name__)

protected_view_staff = partial(protected_view, staff_required=True)

@routes.route("/")
def index():
    return render_template("index.html")

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
    return render_template("payment.html")

@routes.route("/do-payment", methods=["POST"])
def do_payment():
    keys = ["dfirst", "dlast", "dstreet-address", "dpostcode", "cname", "credit-no", "cvc", "month", "year", "bfirst-name", "blast-name", "bstreet-address", "bpostcode"]
    payment = Payment(\
        delivery_first_name=request.form["dfirst"],\
        delivery_last_name=request.form["dlast"],\
        delivery_street_address=request.form["dstreet-address"],\
        delivery_postcode=request.form["dpostcode"],\
        credit_name=request.form["cname"],\
        credit_no=request.form["credit-no"],\
        cvc=request.form["cvc"],\
        month=request.form["month"],\
        year=request.form["year"],\
        bill_first_name=request.form["bfirst-name"],\
        bill_last_name=request.form["blast-name"],\
        bill_street_address=request.form["bstreet-address"],\
        bill_postcode=request.form["bpostcode"],\
    )
    db.session.do(payment)
    db.session.commit()

    return jsonify({'success': True})

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

    pageLength = int(request.form["amount"])
    numPages = math.ceil(len(scoredMovies) / pageLength) #if it's an integer, ceil does nothing, otherwise rounds up for the last page with less movies

    index = int(request.form["page"]) * pageLength
    for movie, score, title in scoredMovies[index : index + pageLength]:
        result += '<div class="movie-cell" id="' + str(movie.id) + '"><img src="' + movie.thumbnail_src + '" alt="' + movie.title + '">\
                   <div class="movie-buttons">'
        if (isStaff):
            result += '<button type="button" class="btn btn-dark edit-movie-btn" data-toggle="tooltip" data-placement="top" title="Edit movie details">\
                           <i class="far fa-edit"></i>\
                         </button>\
                         <div class="spacer-h"></div>\
                         <button type="button" class="btn btn-dark edit-movie-copies-btn" data-toggle="tooltip" data-placement="top" title="Edit copies of this movie">\
                            <i class="fas fa-compact-disc"></i>\
                         </button>\
                         <div class="spacer-h"></div>\
                         <button type="button" class="btn btn-dark delete-movie-btn" data-toggle="tooltip" data-placement="top" title="Delete this movie">\
                            <i class="far fa-trash-alt"></i>\
                         </button>'
        else:
            result += '<button type="button" class="btn btn-dark add-to-order-btn" data-toggle="tooltip" data-placement="top" title="Add to order">\
                           <i class="far fa-plus-square"></i>\
                       </button>'

        result += '</div><div class="movie-description">' + movie.title + '<br>(' + str(movie.release_date.year) + ')</div></div>'

    return jsonify({ "success": True, "gridHtml": result + "</div>", "numPages": numPages})

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

UPLOAD_FOLDER = 'app/static/images/thumbnails'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'tiff', 'gif', 'apng', 'svg', 'bmp'])
def filename_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route("/add-movie")
@protected_view_staff
def add_movie():
    return render_template("add_movie.html", genres=db.session.query(Genre).all(), maturityRatings=db.session.query(MaturityRating).all())

@routes.route("/do-add-movie", methods=["POST"])
@protected_view_staff
def do_add_movie():
    try:
        current_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
        if db.session.query(Movie.id).filter_by(title=request.form["title"], release_date=request.form["release-date"]).scalar() is not None:
            return jsonify({"success": False, "reason": "movie exists"})

        if (request.form["title"] == ""\
        or request.form["release-date"] == ""\
        or "image" not in request.files\
        or request.files["image"].filename == ""\
        or request.form["runtime"] == ""\
        or request.form["maturity-rating"] == ""):
            return jsonify({"success": False, "reason": "incomplete form"})

        file = request.files["image"]
        filename = request.form["title"] + "_" + request.form["release-date"] + "_" + secure_filename("_".join(file.filename.split()))
        movie = Movie(\
            title = request.form["title"],\
            release_date = request.form["release-date"],\
            thumbnail_src = "/static/images/thumbnails/" + filename,\
            runtime = request.form["runtime"],\
            maturity_rating = request.form["maturity-rating"]
        )

        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        for id in request.form.getlist("genres[]"):
            genre = db.session.query(Genre).filter_by(id=id).one()
            movie.genres.append(genre)

        db.session.add(movie)
        db.session.commit()

        return jsonify({ "success": True })
    except Exception as e:
        print(e)
        return jsonify({ "success": False, "reason": "Failed to add movie. An internal server error has occurred." })

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
        if (request.form["title"] == ""\
        or request.form["release-date"] == ""\
        or request.form["runtime"] == ""\
        or request.form["maturity-rating"] == ""):
            return jsonify({ "success": False, "reason": "incomplete form" })

        movie = Movie.query.filter_by(id=request.form["id"]).one()
        movie.title = request.form["title"]
        movie.release_date = request.form["release-date"]
        movie.runtime = request.form["runtime"]
        movie.maturity_rating = request.form["maturity-rating"]

        if request.files["image"].filename != "":
            current_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

            os.remove("app" + movie.thumbnail_src)

            file = request.files["image"]
            filename = movie.title + "_" + movie.release_date + "_" + secure_filename("_".join(file.filename.split()))
            movie.thumbnail_src = "/static/images/thumbnails/" + filename

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        movie.genres = [];
        for id in request.form.getlist("genres[]"):
            genre = db.session.query(Genre).filter_by(id=id).one()
            movie.genres.append(genre)
        db.session.commit()

        return jsonify({ "success": True })
    except Exception as e:
        print("Excpetion:", e)
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
        os.remove("app" + movie.thumbnail_src)
        db.session.delete(movie)
        db.session.commit()
        return jsonify({ "success": True })
    except:
        return 'Something went wrong trying to delete this movie.', 400

@routes.route("/add-to-order/<movieId>")
def add_to_order(movieId):
    pass

@routes.route("/do-add-to-order", methods=["POST"])
def do_add_to_order():
    # try:
        movie = Movie.query.filter_by(id=request.form["id"]).one()

        order = Orders(\
            accountId = g.logged_in_user.id,\
            trackingStatus = "undelivered",\
            methodId = "01a72541-8206-47b6-8480-d32ba518243d",
        )
        order.movies.append(movie)

        db.session.add(order)
        db.session.commit()

        return jsonify({ "success": True })
        #add this movie to an order
    # except Exception as e:
    #     return jsonify({ "success": False, "reason": str(e) })

@routes.route("/shipmentdetails/create", methods=["GET", "POST"])
@protected_view
def create_shipment_details():
    if request.method == "POST":
        shipment_details = ShipmentDetails(
            date=date.fromisoformat(request.form["date"]),
            shipment_method=request.form["shipment_method"],
            address=request.form["address"],
            order_id=uuid.UUID(request.form["order_id"]) if request.form["order_id"] else None
        )
        db.session.add(shipment_details)
        db.session.commit()
        return redirect(url_for("routes.view_shipment_details", id=shipment_details.id))
    return render_template("create_shipment_details.html")

@routes.route("/shipmentdetails/<id>", methods=["GET"])
@protected_view
def view_shipment_details(id):
    shipment_details = db.session.query(ShipmentDetails).get(uuid.UUID(id))
    if not shipment_details:
        return "Error. Shipment Details not found", 404
    return render_template("view_shipment_details.html", shipment_details=shipment_details)

@routes.route("/shipmentdetails/<id>/edit", methods=["GET", "POST"])
@protected_view
def edit_shipment_details(id):
    shipment_details = db.session.query(ShipmentDetails).get(uuid.UUID(id))
    if not shipment_details:
        return "Error. Shipment Details not found", 404
    if request.method == "POST":
        shipment_details.date = date.fromisoformat(request.form["date"])
        shipment_details.shipment_method = request.form["shipment_method"]
        shipment_details.address = request.form["address"]
        shipment_details.order_id = uuid.UUID(request.form["order_id"]) if request.form["order_id"] else None
        db.session.commit()
        return redirect(url_for("routes.view_shipment_details", id=shipment_details.id))
    return render_template("edit_shipment_details.html", shipment_details=shipment_details)


@routes.route("/shipmentdetails/<id>/delete", methods=["GET"])
@protected_view
def delete_shipment_details(id):
    shipment_details = db.session.query(ShipmentDetails).get(uuid.UUID(id))
    if not shipment_details:
        return "Error. Shipment Details not found", 404
    db.session.delete(shipment_details)
    db.session.commit()
    return redirect(url_for("routes.list_shipment_details"))

@routes.route("/shipmentdetails", methods=["GET"])
@protected_view
def list_shipment_details():
    order_id = request.args.get("order_id", None)
    if order_id:
        shipment_details = db.session.query(ShipmentDetails).filter(ShipmentDetails.order_id == uuid.UUID(order_id)).one_or_none()
        if shipment_details:
            return redirect(url_for("routes.view_shipment_details", id=shipment_details.id))
        else:
            shipment_details_list = db.session.query(ShipmentDetails).order_by(ShipmentDetails.date.desc())
            return render_template("list_shipment_details.html", shipment_details_list=shipment_details_list, not_found_id=order_id)


    min_date = date.fromisoformat(request.args.get("min_date", "1970-01-01"))
    max_date = date.fromisoformat(request.args.get("max_date", "9999-12-31"))

    shipment_details_list = db.session.query(ShipmentDetails).filter((ShipmentDetails.date >= min_date) & (ShipmentDetails.date <= max_date)).order_by(ShipmentDetails.date.desc())
    return render_template("list_shipment_details.html", shipment_details_list=shipment_details_list)

@routes.route("/createuser", methods=["GET"])
@protected_view_staff
def create_user():
        return render_template("create_user.html")

@routes.route("/order")
def view_order():
    orderlist = db.session.query(MovieOrderLine).all()
    return render_template("orders.html", orderlist = orderlist)

@routes.route("/order/add")
def add_order():
    return redirect(url_for("routes.browse"))

@routes.route("/orderhistory")
def order_history():
    return render_template("orderhistory.html")
