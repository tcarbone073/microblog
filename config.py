import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    # Here, we attempt to look for the environment variable using
    # `os.environ.get()`. If that fails, we have a fallback specified after the
    # `or` operator.
    
    # Secret key
    SECRET_KEY= os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # Configure a database to be stored in the base directory of the app
    SQLALCHEMY_DATABASE_URI= os.environ.get("DATABASE_URI") or \
        "sqlite:///"+os.path.join(basedir, "app.db")

    # Don't track changes to the database
    SQLALCHEMY_TRACK_MODIFICATIONS= False
