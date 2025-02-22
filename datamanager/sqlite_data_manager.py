from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)

    def get_all_users(self):
        """ Returns a list of all users in the database. """


    def get_user_movies(self, user_id):
        """ Returns a list of all movies of a specific user. """


    def add_user(self):
        """ Adds a new user to the database. """


    def add_movie(self):
        """ Adds a new movie to the database """


    def update_movie(self):
        """ Updates the details of a specific movie in the database """


    def delete_movie(self):
        """ Deletes a specific movie from the database. """