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
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genre.id'), primary_key=True)
)


# Association table
user_movie_association = Table(
    'user_movie_association',
    db.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('movie_id', Integer, ForeignKey('movie.id'))
)




class User(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    movies: Mapped[list["Movie"]] = relationship(secondary=user_movie_association, back_populates="users")

    def __repr__(self):
        return f"Object Type User"

    def __str__(self):
        return f"user name: {self.name}"


class Movie(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)
    poster: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    reviews: Mapped[list["Review"]] = relationship(back_populates="movie")
    director_id: Mapped[int] = mapped_column(ForeignKey('director.id'))
    director: Mapped["Director"] = relationship(back_populates="movies")
    genres: Mapped[list["Genre"]] = relationship(secondary=movie_genre_association, back_populates="movies")
    users: Mapped[list["User"]] = relationship(secondary=user_movie_association, back_populates="movies")

    def __repr__(self):
        return f"Object Type Movie"

    def __str__(self):
        return f"movie title: {self.title}\n"


class Review(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    review_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=True)
    review_text: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship(back_populates="reviews")
    movie: Mapped["Movie"] = relationship(back_populates="reviews")

    def __repr__(self):
        return f"Object Type: Review"

    def __str__(self):
        return f"review user: {self.user}\n review movie: {self.movie.title}"


class Director(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)
    birth: Mapped[str] = mapped_column(nullable=True)
    death: Mapped[str] = mapped_column(nullable=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    movies: Mapped[list["Movie"]] = relationship(back_populates="director")

    def __repr__(self):
        return f"Object Type: Director"

    def __str__(self):
        return f"director name: {self.name}\n"


class Genre(db.Model):
    """  Each instance of mapped_column() generate a Column object """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)
    details: Mapped[str] = mapped_column(nullable=True)
    movies: Mapped[list["Movie"]] = relationship(secondary=movie_genre_association, back_populates="genres")

    def __repr__(self):
        return f"Object Type: Genre"

    def __str__(self):
        return f"genre: {self.name}\n"