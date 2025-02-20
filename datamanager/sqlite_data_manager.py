from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)

    def get_all_users(self):
        pass

    def get_user_movies(self, user_id):
        pass