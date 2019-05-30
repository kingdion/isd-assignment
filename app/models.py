from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid4)
    title = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date(), nullable=False)
    thumbnail_src = db.Column(db.String(150), nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    maturity_rating = db.Column(db.Integer, db.ForeignKey('maturityrating.id'), nullable=False)

    genres = db.relationship('Genre', secondary='moviegenre', back_populates="movies")
    copies = db.relationship('MovieCopy')

    def to_dict(self):
        dict = { 'id': self.id,\
                 'title': self.title,\
                 'release_date': self.release_date,\
                 'release_year': self.release_date.year,\
                 'thumbnail_src': self.thumbnail_src,\
                 'runtime': self.runtime,\
                 'maturity_rating': self.maturity_rating,\
                 'genres': [] }
        for genre in self.genres:
            dict['genres'].append(genre.to_dict())

        return dict

    def __init__(self, title, release_date, thumbnail_src, runtime, maturity_rating):
        self.title = title
        self.release_date = release_date
        self.thumbnail_src = thumbnail_src
        self.runtime = runtime
        self.maturity_rating = maturity_rating

    def __repr__(self):
        return f'Movie: {self.title}, {self.release_date}, {self.thumbnail_src}'

class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(35), nullable=False)

    movies = db.relationship('Movie', secondary='moviegenre', back_populates="genres")

    def to_dict(self):
        return { 'id': self.id, 'name': self.name }

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Genre: {self.name}'

class MaturityRating(db.Model):
    __tablename__ = 'maturityrating'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    maturity_rating = db.Column(db.String(3), nullable=False)

    def __init__(self, maturity_rating):
        self.maturity_rating = maturity_rating

    def __repr__(self):
        return f'MaturityRating: {self.maturity_rating}'

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    street_address = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    join_date = db.Column(db.DateTime(), nullable=False)

    logs = db.relationship('UserAccessLog')

    def __init__(self, first_name, last_name, email, username, password, street_address, postcode, phone_number, is_staff, is_active, join_date):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.street_address = street_address
        self.postcode = postcode
        self.phone_number = phone_number
        self.is_staff = is_staff
        self.is_active = is_active
        self.join_date = join_date

    def __repr__(self):
        return f'Account: {self.first_name} {self.last_name} ({self.username})'

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    accountId = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'), nullable=False)
    tracking_status = db.Column(db.String(50), nullable=False)
    methodId = db.Column(UUID(as_uuid=True), default=uuid4)

    movies = db.relationship('MovieCopy', secondary = 'movieorderline', back_populates="orders")

    def __init__(self, accountId, trackingStatus, methodId):
        self.accountId = accountId
        self.tracking_status = trackingStatus
        self.methodId = methodId

    def __repr__(self):
        return f'Order: {self.id} {self.accountId} {self.tracking_status}'

class UserAccessLog(db.Model):
    __tablename__ = 'useraccesslog'
    id = db.Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False, primary_key=True)
    accountId = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'), nullable=False, primary_key=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    log_type = db.Column(db.String(30), nullable=False)

    def __init__(self, accountId, timestamp, log_type):
        self.accountId = accountId
        self.timestamp = timestamp
        self.log_type = log_type

    def __repr__(self):
        return f'User Access Log {self.accountId} | {self.timestamp}, {self.log_type}'

class MovieGenre(db.Model):
    __tablename__ = 'moviegenre'

    movieId = db.Column(UUID(as_uuid=True), db.ForeignKey('movie.id'), primary_key=True, default=uuid4)
    genreId = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)

    def __repr__(self):
        return f'Movie LinkedTo Genre {self.movieId} <-------> {self.genreId}'

class MovieOrderLine(db.Model):
    __tablename__ = 'movieorderline'

    copyId = db.Column(UUID(as_uuid=True), db.ForeignKey('moviecopy.id'), primary_key=True, default=uuid4)
    orderId = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), primary_key=True, default=uuid4)

    def __repr__(self):
        return f'Movie LinkedTo OrderLine: {self.copyId} <-------> {self.orderId}'

class MovieCopy(db.Model):
    __tablename__ = 'moviecopy'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    movieId = db.Column(UUID(as_uuid=True), db.ForeignKey('movie.id'), primary_key=True, default=uuid4)
    copy_information = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    sold = db.Column(db.Boolean, nullable=False)

    orders = db.relationship('Orders', secondary='movieorderline', back_populates="movies")

    def __repr__(self):
        return f'MovieCopy: {self.copy_information}, {self.price}, {self.sold}'

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    dfirst = db.Column(db.String(20), nullable=False)
    dlast = db.Column(db.String(20), nullable=False)
    dstreet_address = db.Column(db.String(50), nullable=False)
    dpostcode = db.Column(db.String(4), nullable=False)
    cname = db.Column(db.String(20), nullable=False)
    credit_no = db.Column(db.String(16), nullable=False)
    cvc = db.Column(db.String(3), nullable=False)
    month = db.Column(db.String(2), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    bfirst_name = db.Column(db.String(20), nullable=False)
    blast_name = db.Column(db.String(20), nullable=False)
    bstreet_address = db.Column(db.String(50), nullable=False)
    bpostcode = db.Column(db.String(4), nullable=False)
    def __repr__(self):
        return f'Payment: {self.bfirst_name}, {self.bfirst_name}'

class PaymentMethod(db.Model):
    __tablename__ = 'paymentmethod'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    method_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'PaymentMethod: {self.method_name}'

class ShipmentDetails(db.Model):
    __tablename__ = 'shipmentdetails'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    date = db.Column(db.Date(), nullable=False)
    shipment_method = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey("orders.id"), nullable=False)
    order = db.relationship("Orders", backref="shipment_details")

    @validates("address")
    def validate_address(self, key, address):
        assert len(address) > 0
        return address

    @validates("shipment_method")
    def validate_shipment_method(self, key, shipment_method):
        assert shipment_method in ("Express","Standard")
        return shipment_method

    def __repr__(self):
        return f'ShipmentDetails: {self.date}, {self.address}, {self.shipment_method}'
