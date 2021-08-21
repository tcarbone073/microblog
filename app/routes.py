from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user

from app import app
from app.forms import LoginForm
from app.models import User


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Tyler"}
    posts = [
        {
            "author": {"username": "John"},
            "body": "Beautiful day in Portland!"
        },
        {
            "author": {"username": "Susan"},
            "body": "The avengers movie was so cool!"
        }
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():

    # If the user is already logged in and they attempt to navigate to the
    # login page, redirect them to `/index`. The `current_user` variable comes
    # from `flask_login`, representing the client of the request.
    if current_user.is_autherticated:
        return redirect(url_for("index"))

    # Create the form and check to see if the fields were filled out correctly.
    form = LoginForm()
    if form.validate_on_submit():

        # Query the table of users from the database. The `username` is
        # obtained from the form. We use `first()` to return the (single)
        # record.
        user = User.query.filter_by(username=form.username.data).first()

        # If the user is not in the database, or the password was incorrect,
        # flash an error message and redirect to the login page.
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("login"))

        # Log in the user, and redirect to the index
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
        
    # Render the login page
    return render_template("login.html", title="Sign In", form=form)
