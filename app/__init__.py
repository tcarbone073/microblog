from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# Initialize the application and load configuration settings from the
# config.py located in the root of the application directory.
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database object, as well as the another object representing
# the database migration engine
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize the flask login object
login = LoginManager(app)

# The `models` module defines the structure of the database
from app import routes, models

