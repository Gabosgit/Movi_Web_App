""" This script create the tables (models) in a database """
import os
from flask import Flask
""" db and models imported from data_models.py """
from datamanager.data_models import db, User, Movie, Review, Director, Genre

app = Flask(__name__)

# data_folder is el Path to folder data
data_folder = os.path.join(app.root_path, 'data')
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(data_folder, 'sqlite.db')
db.init_app(app)

with app.app_context():
    db.create_all()
print(f"Tables created in the database.")