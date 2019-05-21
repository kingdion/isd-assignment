from app import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid4)
    title = db.Column(db.String(50), nullable=False)
    releaseDate = db.Column(db.Date(), nullable=False)
    thumbnailSrc = db.Column(db.String(150), nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    maturity_rating = db.Column(db.Integer, db.ForeignKey('maturityrating.id'), nullable=False)

    genres = db.relationship('Genre', secondary = 'moviegenre', back_populates="movies")

    def __init__(self, title, releaseDate, thumbnailSrc, runtime):
        self.title = title
        self.releaseDate = releaseDate
        self.thumbnailSrc = thumbnailSrc
        self.runtime = runtime

    def __repr__(self):
        return f'Movie: {self.title}, {self.releaseDate}, {self.thumbnailSrc}'

class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(35), nullable=False)

    movies = db.relationship('Movie', secondary = 'moviegenre', back_populates="genres")

    def to_json(self):
        return {'id': self.id, 'name': self.name}

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
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    street_address = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False)

    def __init__(self, first_name, last_name, email, password, street_address, postcode, is_staff):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.street_address = street_address
        self.postcode = postcode
        self.is_staff = is_staff

    def __repr__(self):
        return f'Account: {self.first_name} {self.last_name}'

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    accountId = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'), nullable=False)
    trackingStatus = db.Column(db.String(50), nullable=False)
    methodId = db.Column(UUID(as_uuid=True), default=uuid4)

    movies = db.relationship('MovieCopy', secondary = 'movieorderline', back_populates="orders")

    def __init__(self, accountId, trackingStatus):
        self.accountId = accountId
        self.trackingStatus = trackingStatus

    def __repr__(self):
        return f'Order: {self.id} {self.accountId} {self.trackingStatus}'

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

    orders = db.relationship('Orders', secondary = 'movieorderline', back_populates="movies")

    def __repr__(self):
        return f'MovieCopy: {self.copy_information}, {self.price}, {self.sold}'

class PaymentMethod(db.Model):
    __tablename__ = 'paymentmethod'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    method_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'PaymentMethod: {self.method_name}'
