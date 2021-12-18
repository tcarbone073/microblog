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

from flask import Flask
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


# Initialize the application and load configuration settings from the
# config.py located in the root of the application directory.
app = Flask(__name__)
app.config.from_object(Config)

# Create flask-mail object.
mail = Mail(app)

# Create flask-bootstrap object
bootstrap = Bootstrap(app)

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
from app import routes, models, errors

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



