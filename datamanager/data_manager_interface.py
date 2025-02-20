""" Defines an interface for our DataManager using Python’s abc (Abstract Base Classes) module """
from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """ Defines methods that every DataManager needs to implement. """
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass