import jwt
import uuid
import math
import os
import datetime
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app, session, g
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

@routes.route("/payment_confirm")
def confirm():
    return render_template("payment_confirm.html")

@routes.route("/do-payment", methods=["POST"])
def do_payment():
    keys = ["dfirst", "dlast", "daddress", "dpostcode", "cname", "creditno", "cvc", "month", "year", "bfirst", "blast", "baddress", "bpostcode"]
    payment = Payment(\
        dfirst=request.form["dfirst"],\
        dlast=request.form["dlast"],\
        daddress=request.form["daddress"],\
        dpostcode=request.form["dpostcode"],\
        credit_name=request.form["cname"],\
        creditno=request.form["creditno"],\
        cvc=request.form["cvc"],\
        month=request.form["month"],\
        year=request.form["year"],\
        bfirst=request.form["bfirst"],\
        blast=request.form["blast"],\
        baddress=request.form["baddress"],\
        bpostcode=request.form["bpostcode"],\
        join_date=datetime.datetime.utcnow()\
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({'success': True})

@routes.route("/payment-confirmation", methods=["POST", "PUT"])
@protected_view
def payment_confirmation():
    try:
        keys = ["dfirst", "dlast", "daddress", "dpostcode", "cname", "creditno", "cvc", "month", "year", "bfirst", "blast", "baddress", "bpostcode"]
        confirm_dfirst=request.form["dfirst"],
        confirm_dlast=request.form["dlast"],
        confirm_daddress=request.form["daddress"],
        confirm_dpostcode=request.form["dpostcode"],
        confirm_credit_name=request.form["cname"],
        confirm_creditno=request.form["creditno"],
        confirm_cvc=request.form["cvc"],
        confirm_month=request.form["month"],
        confirm_year=request.form["year"],
        confirm_bfirst=request.form["bfirst"],
        confirm_blast=request.form["blast"],
        confirm_baddress=request.form["baddress"],
        confirm_bpostcode=request.form["bpostcode"],

        db.session.commit()
    except:
        return jsonify({"success": False, "message": "Something went wrong in confirmation."})

    return jsonify({"success": True, "message": "Your payment details are confirmed!"})


@routes.route("/delete-payment", methods=["POST", "DELETE"])
@protected_view
def delete_payment():
    # Remove payment and move user back to payment detail input
    # return a success response.

    db.session.delete(g.logged_in_user)
    session.pop('token', None)
    db.session.commit()

    return jsonify({"success": True, "message": "Your Payment details have been successfully deleted"})


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

    isStaff = g.logged_in_user.is_staff if g.logged_in_user else False

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
            result += '<button type="button" class="btn btn-dark edit-movie-copies-btn" data-toggle="tooltip" data-placement="top" title="View copies of this movie">\
                           <i class="fas fa-compact-disc"></i>\
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
            elif (sWord in tWord and (len(sWord) > 2 or len(tWord) <= 2)) or (tWord in sWord and (len(tWord) > 2 or len(sWord <= 2))):
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
        return jsonify({ "success": False, "reason": str(e) })

@routes.route("/edit-movie-copies/<movieID>")
def edit_movie_copies(movieID):
    try:
        movie = Movie.query.filter_by(id=movieID).one()
        return render_template("edit_movie_copies.html", movie=movie)
    except:
        return 'Something went wrong trying to edit copies of this movie.', 400

@routes.route("/do-get-movie-copies/<movieID>", methods=["GET"])
def do_get_movie_copies(movieID):
    try:
        copies = []
        movie = Movie.query.filter_by(id=movieID).one()
        for copy in movie.copies.order_by(MovieCopy.sold.desc(), MovieCopy.price.desc()):
            copies.append(copy.to_dict())

        return jsonify({ "success": True, "copies": copies, "isStaff": g.logged_in_user.is_staff if g.logged_in_user else False })
    except Exception as e:
        return jsonify({ "success": False, "reason": str(e) })

@routes.route("/do-add-movie-copy/<movieID>", methods=["POST"])
@protected_view_staff
def do_add_movie_copy(movieID):
    try:
        copy = MovieCopy(movieID, request.form["copy-description"], request.form["copy-price"])
        db.session.add(copy)
        db.session.commit()

        newCopies = []
        movie = Movie.query.filter_by(id=movieID).one()
        for copy in movie.copies:
            newCopies.append(copy.to_dict())

        return jsonify({ "success": True, "copies": newCopies, "isStaff": g.logged_in_user.is_staff if g.logged_in_user else False })
    except Exception as e:
        return jsonify({ "success": False, "reason": str(e) })

@routes.route("/do-delete-movie-copy", methods=["POST"])
@protected_view_staff
def delete_movie_copy():
    try:
        movieCopy = MovieCopy.query.filter_by(id=request.form["id"]).one()
        if movieCopy.sold:
            return jsonify({ "success": False, "reason": "This copy has already been sold and so cannot be deleted." })

        db.session.delete(movieCopy)
        db.session.commit()
        return jsonify({ "success": True, "id": request.form["id"] })
    except Exception as e:
        return jsonify({ "success": False, "reason": str(e) })

@routes.route("/do-edit-movie-copy", methods=["POST"])
@protected_view_staff
def do_edit_movie_copy():
    try:
        if (request.form["copy-id"] == ""\
        or request.form["copy-price"] == ""\
        or request.form["copy-description"] == ""):
            return jsonify({ "success": False, "reason": "incomplete form" })

        copy = MovieCopy.query.filter_by(id=request.form["copy-id"]).one()
        if copy.sold:
            return jsonify({ "success": False, "reason": "This copy has already been sold and so cannot be edited." })

        copy.price = request.form["copy-price"]
        copy.copy_information = request.form["copy-description"]

        db.session.commit()

        return jsonify({ "success": True })
    except Exception as e:
        return jsonify({ "success": False, "reason": str(e) })

@routes.route("/do-delete-movie", methods=["POST"])
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

@routes.route("/do-add-to-order", methods=["POST"])
def do_add_to_order():
    try:
        movie = Movie.query.filter_by(id=request.form["id"]).one()
        #@Amara, this is going to create an order EVERY TIME you add to order, you need to change this so it looks for an existing order first


        order = Orders(\
            accountId = g.logged_in_user.id,\
            trackingStatus = "undelivered",\
            methodId = "01a72541-8206-47b6-8480-d32ba518243d",
        )
        order.movies.append(movie)

        db.session.add(order)
        db.session.commit()
        return jsonify({ "success": True })
    except Exception as e:
        return jsonify({ "success": False, "reason": str(e) })

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

@routes.route("/create_user", methods=["GET"])
@protected_view_staff
def create_user():
        return render_template("create_user.html")

@routes.route("/view_user")
@protected_view_staff
def view_user():
    return render_template("view_user.html", accounts=db.session.query(Account).all())

@routes.route("/modify_user")
@protected_view_staff
def modify_user():
    return render_template("modify_user.html")

@routes.route("/order")
def view_order():
    orderlist = db.session.query(MovieOrderLine).all()
    moviecopylist = db.session.query(MovieCopy).all()
    movielist = db.session.query(Movie).all()
    movieorder = db.session.query(Orders).all()
    return render_template("orders.html", orderlist = orderlist, moviecopylist = moviecopylist, movielist = movielist, movieorder = movieorder)

@routes.route("/order/add")
def add_order():
    return redirect(url_for("routes.browse"))

@routes.route("/orderhistory")
def order_history():
    orderlist = db.session.query(MovieOrderLine).all()
    moviecopylist = db.session.query(MovieCopy).all()
    movielist = db.session.query(Movie).all()
    movieorder = db.session.query(Orders).all()
    return render_template("orderhistory.html", orderlist = orderlist, moviecopylist = moviecopylist, movielist = movielist, movieorder = movieorder)

@routes.route("/do-delete-movie-order", methods=["POST", "DELETE"])
def delete_movie_order():
    try:
        movieOrder = Orders.query.filter_by(id=request.form["movie_id"]).first()
        db.session.delete(movieOrder)
        db.session.commit()
    except:
        return jsonify({'success': False, 'message' : 'Something went wrong trying to remove this movie.'})

    return jsonify({'success': False, 'message' : 'The movie has been removed.'})
