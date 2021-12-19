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
 - Configure settings for mail server, if one is set up
 - Configure logging settings
"""

# Flask and Flask extensions
from flask import Flask
from flask import request
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Builtins
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

# User-defined
from config import Config


# Initialize the application and load configuration settings from the
# config.py located in the root of the application directory.
app = Flask(__name__)
app.config.from_object(Config)

# Create flask-mail object.
mail = Mail(app)

# Create flask-bootstrap object
bootstrap = Bootstrap(app)

# Create flask-moment object
moment = Moment(app)

# Create flask-babel object
babel = Babel(app)

# Initialize the database object, as well as the another object representing
# the database migration engine
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize the flask login object
login = LoginManager(app)
login.login_view = "login"

# Override the default login message with a version wrapped in the
# lazy-processing function.
login.login_message = _l('Please log in to access this page.')

# The `models` module defines the structure of the database. Note here that we
# are importing at the bottom of the file, and not the typical top of the file.
# This is because the `routes` module imports the `app` variable defined above.
# This avoids a circular import.
from app import routes, models, errors

# Select a language translation based on a best-match to the client's
# `Accept-Languages` header.
@babel.localeselector
def get_local():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

# Configurations for production
if not app.debug:

    # Configure mail server
    if app.config["MAIL_SERVER"]:

        auth = None
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost = (app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr = "no-reply@" + app.config["MAIL_SERVER"],
            toaddrs = app.config["ADMINS"],
            subject = "Microblog Failure",
            credentials = auth,
            secure = secure
        )
        
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # Configure logging
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # The RotatingFileHandler class creates a new log file whenever the log
    # file exceeds the `maxBytes` limit. Additionally, `backupCount` denotes
    # how many log files are backed up.
    file_handler = RotatingFileHandler("logs/microblog.log", maxBytes=10240,
        backupCount=10)

    # Set the format of the log messages
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Microblog")



