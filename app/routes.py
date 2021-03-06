"""
This module contains all of the different URLs that the application implements.
Each URL page is handled with what is called a 'view' function.

The basic operation of a view function is that when the web browser requests a
URL, flask is going to call the corresponding view function, passing the return
value back to the web browser. Each view function uses the `render_template`
function to pass dynamic content to the template as keyword arguments. The
Jinja2 template engine renders the content.
"""

from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.email import send_password_reset_email
from app.forms import (
    EditProfileForm,
    EmptyForm,
    LoginForm,
    PostForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetPasswordRequestForm,
)
from app.models import Post, User


@app.before_request
def before_request():
    """
    Executed before any view function is called.
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    # Create a post
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_("Your post is now live!"))
        return redirect(url_for("index"))

    # Default to show page 1
    page = request.args.get("page", 1, type=int)

    # Display posts of other users that we are following
    posts = current_user.followed_posts().paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )

    # Establish URL for next page, if one exists
    if posts.has_next:
        next_url = url_for("index", page=posts.next_num)
    else:
        next_url = None

    # Establish URL for previos page, if one exists
    if posts.has_prev:
        prev_url = url_for("index", page=posts.prev_num)
    else:
        prev_url = None

    return render_template(
        "index.html",
        title="Home",
        form=form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    # If the user is already logged in and they attempt to navigate to the
    # login page, redirect them to `/index`. The `current_user` variable comes
    # from `flask_login`, representing the client of the request.
    if current_user.is_authenticated:
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

        # If the user was redirected to the login page from a page they were
        # unable to view before logging in, redirect them back to that page.
        # Otherwise, bring them to the index.
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    # Render the login page
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")

        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get("page", 1, type=int)

    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )

    # Establish URL for next page, if one exists
    if posts.has_next:
        next_url = url_for("user", username=user.username, page=posts.next_num)
    else:
        next_url = None

    # Establish URL for previos page, if one exists
    if posts.has_prev:
        prev_url = url_for("user", username=user.username, page=posts.prev_num)
    else:
        prev_url = None

    form = EmptyForm()

    return render_template(
        "user.html",
        user=user,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form,
    )


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    # If the data is validated, copy into the user object and write to the
    # database.
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))

    # There can be two cases where the data isn't validated: when the browser
    # sends a GET request, in which case an initial version of the form needs
    # to be provided. The other case is if the browser sends a POST request
    # with form data, but something is wrong with the data.
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", title="Edit Profile", form=form)


@app.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_("User %(username)s not found", username=username))
            return redirect(url_for("index"))

        if user == current_user:
            flash("You cannot follow yourself.")
            return redirect(url_for("user", username=username))

        current_user.follow(user)
        db.session.commit()
        flash("You are now following {}.".format(username))
        return redirect(url_for("user", username=username))

    else:
        return redirect(url_for("index"))


@app.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash(_("User %(username)s not found", username=username))
            return redirect(url_for("index"))

        if user == current_user:
            flash("You cannot unfollow yourself.")
            return redirect(url_for("user", username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash("You are now following {}.".format(username))
        return redirect(url_for("user", username=username))
    else:
        return redirect(url_for("index"))


@app.route("/explore")
@login_required
def explore():

    # Default to show page 1
    page = request.args.get("page", 1, type=int)

    # Get all posts by all users. Paginate accordingly.
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )

    # Establish URL for next page, if one exists
    if posts.has_next:
        next_url = url_for("explore", page=posts.next_num)
    else:
        next_url = None

    # Establish URL for previos page, if one exists
    if posts.has_prev:
        prev_url = url_for("explore", page=posts.prev_num)
    else:
        prev_url = None

    # Use the same template as the main page of the app ('index.html'), but do
    # not pass in the form argument
    return render_template(
        "index.html",
        title="Explore",
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():

    # If the user is logged in, no need to send password reset email.
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            send_password_reset_email(user)

        # Flash this message even if the user is unkown. This is so clients
        # cannot use this form to determine if a given user is a member or not.
        flash("Check your email for the instruction to reset your password.")

        return redirect(url_for("login"))

    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    user = User.verify_reset_password_token(token)

    if not user:
        return redirect(url_for("index"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("login"))

    return render_template("reset_password.html", form=form)
