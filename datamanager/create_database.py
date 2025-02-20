""" This script create the tables (models) in a database """
from flask import Flask
""" db and models imported from data_models.py """
from data_models import db, User, Movie, Review, Director, Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/sqlite.db'
db.init_app(app) # initiation of the db with the app.

with app.app_context():
    db.create_all()

print(f"Tables created in the database.")