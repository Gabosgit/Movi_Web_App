"""
    API of the Movi Web App
"""
from flask import Blueprint, jsonify, request
from datamanager.data_models import db, User, Movie, Review, Director, user_movie_association


api = Blueprint('api', __name__)


def add_director_return_record_id(director_name):
        add_director_record = Director(
            name=director_name
        )
        db.session.add(add_director_record)
        db.session.commit()  # commits the session to the DB.
        id_director = add_director_record.id
        return id_director

@api.route('/users', methods=['GET'])
def get_users():
    """ Gets all users registered in the database """
    users = User.query.all()
    user_list = [{"id": user.id, "name": user.name} for user in users]
    print(user_list)
    return jsonify(user_list)


@api.route('/users/<user_id>/movies', methods=['GET'])
def get_user_favorite_movies(user_id):
    """ Gets the favorite movies of a user by user_id"""
    user_movies = db.session.query(Movie).join(user_movie_association, Movie.id == user_movie_association.c.movie_id).filter(user_movie_association.c.user_id == user_id).all()
    movies_list = [{
        "id": movie.id,
        "title": movie.title,
        "genre": movie.genre,
        "year": movie.year,
        "director": movie.director.name}
        for movie in user_movies]

    return jsonify(movies_list)


@api.route('/add_movie/<user_id>/movie', methods=['POST'])
def add_movie_for_a_user(user_id):
    """ Add a movie to a favorite movies list of a user """

    if request.method == 'POST':
        #return jsonify('HELLOW')
        title = request.form.get('title')
        genre = request.form.get('genre')
        year = request.form.get('year')
        rating = request.form.get('rating')
        poster = request.form.get('poster')
        description = request.form.get('description')
        director = request.form.get('director')


        if director:
            director_id = add_director_return_record_id(director)
        else:
            director_id = 'N/A'
        if not genre:
            genre = 'N/A'
        if not year:
            year = 'N/A'
        if not rating:
            rating = 'N/A'
        if not poster:
            poster = 'N/A'
        if not description:
            description = 'N/A'


        add_movie_record = Movie(
            title=title,
            genre=genre,
            year=year,
            rating=rating,
            poster=poster,
            director_id=director_id,
            description=description
        )
        movie_info = {
            'title': title,
            'genre': genre,
            'year': year,
            'rating': rating,
            'poster': poster,
            'director_id': director_id,
            'description': description
        }

        db.session.add(add_movie_record)
        db.session.commit()  # commits the session to the DB.
        id_new_movie = add_movie_record.id

        user = User.query.get(user_id)
        movie = Movie.query.get(id_new_movie)

        if user and movie:
            user.movies.append(movie)
            db.session.commit()
            return jsonify(movie_info)
        else:
            return False
