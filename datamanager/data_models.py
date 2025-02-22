from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Table, Column, Integer, ForeignKey


""" SQLAlchemy() creates a db object. 
From this object we will be able to create tables with a model 'parent class' (db.Model) """
db = SQLAlchemy()

# Partnership table for Movie-Genre
movie_genre_association = Table(
    'movie_genre_association',
    db.metadata,
    Column('movie_id', Integer, ForeignKey('movie.movie_id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genre.genre_id'), primary_key=True)
)


# Association table
user_movie_association = Table(
    'user_movie_association',
    db.metadata,
    Column('user_id', Integer, ForeignKey('user.user_id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.movie_id'), primary_key=True)
)


class User(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(nullable=False)
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    movies: Mapped[list["Movie"]] = relationship(secondary=user_movie_association, back_populates="users")

    def __repr__(self):
        return f"{self.user_name}"

    def __str__(self):
        return (f"user_name: {self.user_name}\n")


class Movie(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    movie_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    movie_title: Mapped[str] = mapped_column(nullable=False)
    movie_genre: Mapped[str] = mapped_column(nullable=True)
    release_year: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)
    reviews: Mapped[list["Review"]] = relationship(back_populates="movie")
    director_id: Mapped[int] = mapped_column(ForeignKey('director.director_id'))
    director: Mapped["Director"] = relationship(back_populates="movies")
    genres: Mapped[list["Genre"]] = relationship(secondary=movie_genre_association, back_populates="movies")
    users: Mapped[list["User"]] = relationship(secondary=user_movie_association, back_populates="movies")

    def __repr__(self):
        return f"{self.movie_title}"

    def __str__(self):
        return (f"movie_title: {self.movie_title}\n")


class Review(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    review_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.movie_id'), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=True)
    review_text: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship(back_populates="reviews")
    movie: Mapped["Movie"] = relationship(back_populates="reviews")

    def __repr__(self):
        return f"{self.review_text}"

    def __str__(self):
        return (f"review_text: {self.review_text}")


class Director(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    director_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    director_name: Mapped[str] = mapped_column(nullable=True)
    director_birth: Mapped[str] = mapped_column(nullable=True)
    director_bio: Mapped[str] = mapped_column(nullable=True)
    movies: Mapped[list["Movie"]] = relationship(back_populates="director")

    def __repr__(self):
        return f"{self.director_name}"

    def __str__(self):
        return (f"director_name: {self.director_name}\n")


class Genre(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    genre_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    genre_name: Mapped[str] = mapped_column(nullable=True)
    genre_details: Mapped[str] = mapped_column(nullable=True)
    movies: Mapped[list["Movie"]] = relationship(secondary=movie_genre_association, back_populates="genres")

    def __repr__(self):
        return f"{self.genre_name}"

    def __str__(self):
        return (f"genre_name: {self.genre_name}\n")