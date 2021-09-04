"""
This is where the flask application starts. One of the functions of the `flask
run` command-line tool is to attempt to `import app`. Because the name of the
package associated with this file is named `app`, this script is called to
initiate the application.

Functions performed by this fie include:
 - Importing configuration settings from `config.py` in the project root
   directory
 - Initializing database objects
 - Importing the `routes.py` module, which contains all of the website URLs
   (i.e., view functions)
"""

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
login.login_view = "login"

# The `models` module defines the structure of the database. Note here that we
# are importing at the bottom of the file, and not the typical top of the file.
# This is because the `routes` module imports the `app` variable defined above.
# This avoids a circular import.
from app import routes, models

