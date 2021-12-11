"""
This module contains classes that represent database tables. The ORM layer of
the SQLAlchemy translates rows of the tables to objects created from these
classes.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import hashlib
from datetime import datetime
from time import time
import jwt

from app import db, login, app


# This table is created outside of a model class, becuase it is an auxiliary
# table that has no data other than foreign keys for other table entries (in
# this case, user IDs)
followers = db.Table("followers", 
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
)


class User(UserMixin, db.Model):
    """
    Represents one user (i.e., row) of a table of users in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # This defines a 'one-to-many' relationship. The first argument represents
    # the 'many' side of the relationship. The `backref` argument defines the
    # name of the field that will be added to the objects of the 'many' class
    # that points back at the 'one' objects (in this case, adding a
    # `post.author` that returns the user, given a post). The `lazy` argument
    # is... TBD.
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    # This defines a many-to-many relationship for other uses that follow this
    # user (i.e., linking `User` instances to other `User` instances).
    followed = db.relationship(
        "User",
        secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = db.backref("followers", lazy="dynamic"),
        lazy="dynamic"
    )

    def __repr__(self):
        """How objects of this class are printed."""
        return "<User %s>" % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """Return URL for the user's avatar image"""
        digest = hashlib.md5(self.email.lower().encode("utf-8")).hexdigest()

        url = "https://www.gravatar.com/avatar/{}?d=identicon&s={}"
        return url.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        """
        Return a query of all posts by users that we are following, along with
        our own posts, sorted by most recent date.
        """
        
        # Here, we join the 'followers' table and the 'posts' table by matching
        # the 'followed-by' user and the user the created the post. We filter
        # the resultant table by only the posts created by users that we are
        # following.
        followed_posts = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)

        # Get all posts that we created
        own_posts = Post.query.filter_by(user_id = self.id)

        # Return the union of the two queries, sorted by the date that the post
        # was created.
        return followed_posts.union(own_posts).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id, 
                'exp': time() + expires_in
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
            )
        
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                    algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)




class Post(db.Model):
    """
    Represents a post by a user to the blog.
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Post %s>" % self.body

@login.user_loader
def load_user(id):
    """
    The `user_loader` function keeps track of users that have logged into the
    application.
    """
    return User.query.get(int(id))


