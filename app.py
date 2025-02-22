from flask import Flask, render_template, request, redirect
from datamanager.data_models import db, User, Movie, Review, Director, Genre, user_movie_association
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)

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


@app.route('/')
def home():
    """ home page of the application """

    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def list_users():
    """ Presents a list of all users registered in the Movie Web App"""
    # Example within a Flask route or a function with an app context:
    with app.app_context():
        if request.method == 'POST':
            search_name = request.form.get('search_name')

            if search_name:
                users = User.query.filter(User.user_name.like(f"%{search_name}%")).all()
            else:
                # Get all records from the 'User' table
                users = User.query.all()
            return render_template('users.html', users=users)


    # Get all records from the 'User' table
    users = User.query.all()

            # Access other attributes of the User object as needed
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movies(user_id):
    """ Exhibits a specific user’s list of favorite movies.
        Uses the <user_id> to fetch the appropriate user’s movies."""
    data = {
        'poster_url': '',
        'title': "NOT FOUND",
        'year': '',
        'genre': '',
        'director': '',
        'rating': ''
    }

    user = User.query.get(user_id)
    movies = user.movies
    for movie in movies:
        print(movie.movie_title, movie.movie_genre, movie.release_year, movie.rating, movie.director)
    print()
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """ Presents a form that enables the addition of a new user to the Movie Web App """
    if request.method == 'POST':
        new_user_name = request.form.get('user_name')
        new_user = User(user_name = new_user_name)
        if new_user_name:
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()  # commits the session to the DB.
            return redirect('/users')

    return render_template('add_user.html')


def get_needed_data(data_movie):
    """ Filter the necessary data from the external IPA """
    poster_url = data_movie['Poster']
    title = data_movie['Title']
    year = data_movie['Year']
    genre = data_movie['Genre']
    director = data_movie['Director']

    try:
        rating = float(data_movie['Ratings'][0]['Value'][:-3])
    except IndexError as e:
        print(e)
        rating = 'N/A'

    data = {
        'poster_url': poster_url,
        'title': title,
        'year': year,
        'genre': genre,
        'director': director,
        'rating': rating
    }
    return data


def add_director_return_record_id(director_name):
    with app.app_context():
        add_director_record = Director(
            director_name=director_name
        )
        db.session.add(add_director_record)
        db.session.commit()  # commits the session to the DB.
        id_director = add_director_record.director_id
        return id_director


 # Function to add a connection


def add_movie_return_record_id(director_id, data):
    with app.app_context():
        add_movie_record = Movie(
            movie_title=data['title'],
            movie_genre=data['genre'],
            release_year=data['year'],
            rating=data['rating'],
            director_id=director_id
        )

        db.session.add(add_movie_record)
        db.session.commit()  # commits the session to the DB.
        id_new_movie = add_movie_record.movie_id
        return id_new_movie


def connect_user_movie(user_id, id_new_movie):
    with app.app_context():
        user = User.query.get(user_id)
        movie = Movie.query.get(id_new_movie)

        if user and movie:
            user.movies.append(movie)
            db.session.commit()
            return True
        else:
            return False


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    msg = ''
    user = User.query.get(user_id)
    data = {}

    if request.method == 'POST':
        movie_title = request.form.get('movie_title')
        add_this_movie = request.form.get('add_this_movie')
        print(user)
        from_ipa_fetched_data = fetch_data(movie_title)
        data = get_needed_data(from_ipa_fetched_data)

        if not movie_title is None:
            if from_ipa_fetched_data['Response'] == 'False':
                data = {
                    'poster_url': '',
                    'title': "NOT FOUND",
                    'year': '',
                    'genre': '',
                    'director': '',
                    'rating': ''
                }
                msg =f'No movie with the search entry "{movie_title}" was found.'
            else:
                data = get_needed_data(from_ipa_fetched_data)
                msg = f'Here is the film found with the search entry "{movie_title}"'

            return render_template('add_movie.html', user_id=user_id, user_name=user.user_name, data=data, msg=msg)

        if add_this_movie:
            from_ipa_fetched_data = fetch_data(add_this_movie)
            data = get_needed_data(from_ipa_fetched_data)
            msg = f'"{add_this_movie}" was added to your movie list!'

            # External function
            id_director = add_director_return_record_id(data['director'])

            # External function
            id_new_movie = add_movie_return_record_id(id_director, data)

            # Adds the movie in the association list user.movies
            connect_user_movie(user_id, id_new_movie)

            return render_template("user_movies.html", user_id=user_id, user=user, data=data, msg=msg)

    return render_template('add_movie.html', user_id=user_id, user_name=user.user_name, data=data, msg=msg)


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie():
    """ displays a form allowing for the updating of details of a specific movie in a user’s list """
    pass


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie():
    """ Upon visiting this route, a specific movie will be removed from a user’s favorite movie list """
    pass



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)