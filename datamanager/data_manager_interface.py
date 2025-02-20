""" Defines an interface for our DataManager using Python’s abc (Abstract Base Classes) module """
from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """ Defines methods that every DataManager needs to implement. """
    @abstractmethod
    def get_all_users(self):
        """ Returns a list of all users in the database. """
        pass


    @abstractmethod
    def get_user_movies(self, user_id):
        """ Returns a list of all movies of a specific user. """
        pass


    @abstractmethod
    def add_user(self):
        """ Adds a new user to the database. """
        pass


    @abstractmethod
    def add_movie(self):
        """ Adds a new movie to the database """
        pass


    @abstractmethod
    def update_movie(self):
        """ Updates the details of a specific movie in the database """
        pass


    @abstractmethod
    def delete_movie(self):
        """ Deletes a specific movie from the database. """
        pass