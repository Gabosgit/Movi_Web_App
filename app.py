"""
Movi Web App allows to create users and set a list of favorite movies.
It is possible to fetch information of the movie with artificial intelligent
"""
from flask import Flask, render_template, request, redirect, jsonify
from datamanager.data_models import db, User, Movie, Review, Director, user_movie_association
import os
from dotenv import load_dotenv
import requests
from datamanager.gemini_ai import fetch_from_gemini
from sqlalchemy import desc, delete
from api import (api)  # Importing the API blueprint

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')  # Registering the blueprint

# data_folder is el Path to folder data
data_folder = os.path.join(app.root_path, 'data')
""" data_manager allows to interact with the data. """
# Use the appropriate path to your Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(data_folder, 'sqlite.db')
db.init_app(app)

#loads variables from the .env file into the environment
load_dotenv()
# os.getenv() to access the environment variables loaded from the .env file
API_KEY = os.getenv('API_KEY')


def fetch_data(movie_title):
    """ Receives a 'movie_title' from the user as an argument.
        Gets the movie information from the API by request GET.
        If the response is 'OK' returns the movie infos as json data,
        if not, prints an error in the terminal """
    API_URL = f'https://www.omdbapi.com/?apikey={API_KEY}&t={movie_title}'
    response = requests.get(API_URL)
    if response.status_code == requests.codes.ok:
        json_data = response.json()
        return json_data
    else:
        print("Error:", response.status_code, response.text)
        return False


def get_needed_data(data_movie):
    """ Filter the necessary data from the external IPA """
    if data_movie['Response'] == 'False':
        data = {
            'poster_url': '',
            'title': "NOT FOUND",
            'year': '',
            'genre': '',
            'director': '',
            'rating': '',
            'description': ''
        }
    else:
        poster = data_movie['Poster']
        title = data_movie['Title']
        year = data_movie['Year']
        genre = data_movie['Genre']
        director = data_movie['Director']
        description = data_movie['Plot']

        try:
            rating = float(data_movie['Ratings'][0]['Value'][:-3])
        except IndexError as e:
            print(e)
            rating = 'N/A'

        data = {
            'poster': poster,
            'title': title,
            'year': year,
            'genre': genre,
            'director': director,
            'rating': rating,
            'description': description
        }
    return data


def add_director_return_record_id(director_name):
    """ Get the director_name and insert a record in the director table. Return the id of this new record """
    with app.app_context():
        add_director_record = Director(
            name=director_name
        )
        db.session.add(add_director_record)
        db.session.commit()  # commits the session to the DB.
        id_director = add_director_record.id
        return id_director


def add_movie_return_record_id(director_id, data):
    """ Gets the director_id and the data of the new movie.
        Insert the movie with all information in the table Movies.
        Return the ID of the new movie table record.
    """
    with app.app_context():
        add_movie_record = Movie(
            title=data['title'],
            genre=data['genre'],
            year=data['year'],
            rating=data['rating'],
            poster=data['poster'],
            director_id=director_id,
            description=data['description']
        )

        db.session.add(add_movie_record)
        db.session.commit()  # commits the session to the DB.
        id_new_movie = add_movie_record.id
        return id_new_movie


def connect_user_movie(user_id, id_new_movie):
    """ Insert a record in the association table user_monies_association connecting the user_id with the new movie id """
    with app.app_context():
        user = User.query.get(user_id)
        movie = Movie.query.get(id_new_movie)

        if user and movie:
            user.movies.append(movie)
            db.session.commit()
            return True
        else:
            return False


def update_info(data, movie):
    """
        Get a movie and the new data to update.
        Put the data content in a dictionary
        Update the data to the movie and commit the changes
    """
    update_data = {}
    for k, v in data.items():
        update_data[k] = v

    if update_data['description']:
        movie.description = update_data['description']
    if update_data['rating']:
        movie.rating = update_data['rating']
    if update_data['genre']:
        movie.genre = update_data['genre']
    if update_data['bio']:
        movie.director.bio = update_data['bio']
    if update_data['birth']:
        movie.director.birth = update_data['birth']
    if update_data['death']:
        movie.director.death = update_data['death']
    db.session.commit()


def get_reviews_by_movie_id(movie_id):
    """Gets the reviews for a specific movie_id."""
    try:
        reviews = db.session.query(Review).filter_by(movie_id=movie_id).order_by(desc(Review.review_id)).all()
        return reviews
    except Exception as e:
        print(f"Error al obtener reseñas: {e}")
        return []


def movie_reviews(movie_id):
    """Gets the reviews and usernames for a movie_id."""
    # Gets review by movie_id
    reviews = db.session.query(Review).filter_by(movie_id=movie_id).order_by(desc(Review.review_id)).all()

    user_names = {}  # Dictionary for storing usernames

    for review in reviews:
        # Iterates User filtering by id taking the id from review_user_id
        user = db.session.query(User).filter_by(id=review.user_id).first()
        if user:
            user_names[review.user_id] = user.name
        else:
            user_names[review.user_id] = "No user"

    return user_names


def delete_reviews_by_user_id(user_id):
    """Deletes all reviews associated with a given user_id."""
    try:
        with db.session() as session:
            session.execute(delete(Review).where(Review.user_id == user_id))
            session.commit()
        print(f"Reviews for user_id {user_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting reviews for user_id {user_id}: {e}")
        db.session.rollback()


@app.route('/')
def home():
    """ home page of the application """
    return render_template('index.html', display='none')


@app.route('/users', methods=['GET', 'POST'])
def list_users():
    """ Presents a list of all users registered in the Movie Web App"""
    if request.method == 'POST':
        user_id_to_delete = request.form.get('user_id')

        if user_id_to_delete:
            delete_reviews_by_user_id(user_id_to_delete)
            user_to_delete = db.get_or_404(User, user_id_to_delete)
            db.session.delete(user_to_delete)
            db.session.commit()

            msg = f'{user_id_to_delete} | {user_to_delete.name}" was deleted from the users list.'
            users = User.query.all()
            return render_template('users.html', users=users, msg=msg)

    with app.app_context():
        if request.method == 'POST':
            search_name = request.form.get('search_name')

            if search_name:
                users = User.query.filter(User.name.like(f"%{search_name}%")).all()
                msg = f"Select a user from the list. Or click Start."
                if not users:
                    msg = f"No user was found with the name {search_name}"
                    users = User.query.all()
            else:
                # Get all records from the 'User' table
                users = User.query.all()
                msg = "Select a user from the list. Or click Start."
            return render_template('users.html', users=users, msg=msg)


    # Get all records from the 'User' table
    users = User.query.all()
    msg = "Select a user from the list. Or click Start."

            # Access other attributes of the User object as needed
    return render_template('users.html', users=users, msg=msg)


@app.route('/users/<user_id>')
def user_movies(user_id):
    """
        Uses the <user_id> to fetch the appropriate user’s movies.
        Shows a specific user’s list of favorite movies.
    """
    user = User.query.get(user_id)
    # Sort user movies by user_movie_association ID
    # The last movie added is the first one listed
    movies = (
        db.session.query(Movie)
        .join(user_movie_association, Movie.id == user_movie_association.c.movie_id)
        .filter(user_movie_association.c.user_id == user_id)
        .order_by(user_movie_association.c.id.desc())  # Added .desc() here
        .all()
    )
    count_user_movies = len(movies)

    return render_template('user_movies.html', user=user, movies=movies, count_user_movies=count_user_movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """ Presents a form that enables the addition of a new user to the Movie Web App """
    if request.method == 'POST':
        new_user_name = request.form.get('user_name')
        new_user = User(name = new_user_name)
        if new_user_name:
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()  # commits the session to the DB.
            return redirect('/users')

    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
        Gets the id of a user and retrieves it from the database.
        By POST request it gets a movie title and searches for the movie in the API.
        If the movie title is not found in the API it raises a notification.
        If the title exists in the API it displays the found movie.
        By POST request it gets a confirmation of the movie to add in the user's movie list.
        Before adding the movie, it adds the name of the director in the director table to add the id of the director in the new record in the movie table.
        The function does not add the movie if it already exists in the movie table.
        The function does not add the movie to the user's movie list if the movie already exists.
    """
    msg = ''
    user = User.query.get(user_id)
    data = {}

    if request.method == 'POST':
        movie_title = request.form.get('movie_title')
        add_this_movie = request.form.get('add_this_movie')
        from_ipa_fetched_data = fetch_data(movie_title)
        data = get_needed_data(from_ipa_fetched_data)


        if not movie_title is None:
            data = get_needed_data(from_ipa_fetched_data)
            if from_ipa_fetched_data['Response'] == 'False':
                msg = {'text': f'No movie with the search entry "{movie_title}" was found.',
                       'color': 'red'}
            else:
                msg = {'text': f'Here is the movie found with the search entry "{movie_title}"',
                       'color': '#56ABB3'}

            return render_template('add_movie.html', user_id=user_id, user=user, movie=data, msg=msg)

        elif add_this_movie:
            from_ipa_fetched_data = fetch_data(add_this_movie)
            data = get_needed_data(from_ipa_fetched_data)
            title_in_db = data['title']
            movie_in_db = db.session.query(Movie).filter(Movie.title == title_in_db).first()
            title_in_user_movies = [movie.title for movie in user.movies]
            if title_in_db in title_in_user_movies:
                print("ALREADY IN THE LIST")
                msg = {'text': f"The movie {title_in_db} is already in your favorite movies list",
                       'color': "orange"
                       }

                return render_template('add_movie.html', user_id=user_id, user=user, movie=data, msg=msg)

            elif movie_in_db:
                id_movie_in_db = movie_in_db.id
                connect_user_movie(user_id, id_movie_in_db)

            else:
                msg = f'"{add_this_movie}" was added to your movie list!'

                # External function
                id_director = add_director_return_record_id(data['director'])

                # External function
                id_new_movie = add_movie_return_record_id(id_director, data)

                # Adds the movie in the association list user.movies
                connect_user_movie(user_id, id_new_movie)

            # sort movies descending
            movies = (
                db.session.query(Movie)
                .join(user_movie_association, Movie.id == user_movie_association.c.movie_id)
                .filter(user_movie_association.c.user_id == user_id)
                .order_by(user_movie_association.c.id.desc())  # Added .desc() here
                .all()
            )
            count_user_movies = len(movies)

            return render_template("user_movies.html", user_id=user_id, user=user, movies=movies, msg=msg, count_user_movies=count_user_movies)

    return render_template('add_movie.html', user_id=user_id, user=user, movie=data, msg=msg)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    """ Upon visiting this route, a specific movie will be removed from a user’s favorite movie list """
    user = db.session.query(User).get(user_id)
    movie = db.session.query(Movie).get(movie_id)
    movie_to_delete = request.form.get('delete')
    msg = f'Are you sure you want to delete this movie from your favourite movies.'


    if movie_to_delete == 'delete':
        if user and movie:
            user.movies.remove(movie)  # Remove the movie from the users movie list.
            db.session.commit()
            msg = f'The film " {movie.title} " was deleted from your favorite movies list.'
            return render_template('delete_movie.html', movie=movie, user=user, msg=msg, display='none')
        else:
            print("User or Movie Not found")
            return False
    return render_template('delete_movie.html', movie=movie, user=user, msg=msg)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """ displays a form allowing for the updating of details of a specific movie in a user’s list """
    movie = db.get_or_404(Movie, movie_id)
    user = db.get_or_404(User, user_id)
    bio = movie.director.bio
    msg = "Click Submit to save the new data"


    if request.method == 'POST':
        data = request.get_json()  # Parse the JSON from the request body
        prompt = data.get('prompt')  # Access the 'prompt' value

        if not prompt:
            update_info(data, movie)
            print("SE ACTUALIZÒ")
            return jsonify({'response': "FINE"}), 200

        if prompt == 'bio':
            prompt = f"Get a short text about the biography of the director of the movie '{movie.title}', '{movie.director.name}'."
            birth = f"Get only the birthday data without extra text in the format day/month/year of the director of the movie '{movie.title}', '{movie.director.name}'."
            death = f"Get only the death day data without any extra text in the format day/month/year of the director of the movie '{movie.title}', '{movie.director.name}'."
            try:
                response = fetch_from_gemini(prompt)
                birthday = fetch_from_gemini(birth)
                death_day = fetch_from_gemini(death)
                return jsonify({"response": response.text, "birth": birthday.text, "death": death_day.text})
            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                return jsonify({"error": "Failed to generate text"}), 500

        elif prompt == 'description':
            prompt = f"Get a short text about the movie '{movie.title}' of the director '{movie.director.name}'."
            try:
                response = fetch_from_gemini(prompt)
                return jsonify({"response": response.text})
            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                return jsonify({"error": "Failed to generate text"}), 500


    return render_template('update_movie.html', user=user, movie=movie, bio=bio, msg=msg)


@app.route('/info/movie/<movie_id>/user/<user_id>', methods=['GET', 'POST'])
def info_movie(movie_id, user_id):
    """ Retrieves the movie data and shows the information """
    movie = db.get_or_404(Movie, movie_id)
    user = db.get_or_404(User, user_id)
    reviews = get_reviews_by_movie_id(movie_id)
    dict_review_usernames = movie_reviews(movie_id)

    return render_template('info_movie.html', movie=movie, user=user, reviews=reviews, dict_review_usernames=dict_review_usernames)


@app.route('/review/user/<user_id>/movie/<movie_id>/', methods=['GET', 'POST'])
def add_review(movie_id, user_id):
    """
        Add the user's rating and review in the review table
        The reviews are shown in the movie's INFO section.
    """
    movie = db.get_or_404(Movie, movie_id)
    user = db.get_or_404(User, user_id)

    if request.method == 'POST':
        new_review = request.form.get('new_review')
        user_rating = request.form.get('user_rating')

        new_review = Review(
            user_id=user_id,
            movie_id=movie_id,
            rating=user_rating,
            text=new_review
        )
        with app.app_context():
            db.session.add(new_review)
            db.session.commit()  # commits the session to the DB.
        return redirect(f'/info/movie/{movie_id}/user/{user_id}')


    return render_template('add_review.html', movie=movie, user=user)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)