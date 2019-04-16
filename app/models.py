from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from uuid import uuid4

class Movie(db.Model):
    __tablename__ = 'movie'
    
    id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid4)
    title = db.Column(db.String(50), nullable=False)
    releaseDate = db.Column(db.Date(), nullable=False)
    thumbnailSrc = db.Column(db.String(150), nullable=False)

    genres = db.relationship('Genre', secondary = 'moviegenre', back_populates="movies")
    orders = db.relationship('Orders', secondary = 'movieorder', back_populates="movies")

    def __init__(self, title, releaseDate, thumbnailSrc):
        self.title = title
        self.releaseDate = releaseDate
        self.thumbnailSrc = thumbnailSrc

    def __repr__(self):
        return f'Movie: {self.title}, {self.releaseDate}, {self.thumbnailSrc}'

class Genre(db.Model):
    __tablename__ = 'genre'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)

    movies = db.relationship('Movie', secondary = 'moviegenre', back_populates="genres")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Genre: {self.name}'

class Account(db.Model):
    __tablename__ = 'account'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email 
        self.password = password

    def __repr__(self):
        return f'Account: {self.first_name} {self.last_name}'

class Orders(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    accountId = db.Column(UUID(as_uuid=True), db.ForeignKey('account.id'))
    trackingStatus = db.Column(db.String(50), nullable=False)
   
    movies = db.relationship('Movie', secondary = 'movieorder', back_populates="orders")

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
        return f'{self.movie} <-------> {self.genre}'

class MovieOrder(db.Model):
    __tablename__ = 'movieorder'

    movieId = db.Column(UUID(as_uuid=True), db.ForeignKey('movie.id'), primary_key=True, default=uuid4)
    orderId = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), primary_key=True, default=uuid4)

    def __repr__(self):
        return f'{self.order} <-------> {self.movie}'
