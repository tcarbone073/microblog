from app import db
from datetime import datetime

class User(db.Model):
     """
     Represents one user (i.e., row) of a table of users in the database.
     """
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(64), index=True, unique=True)
     email = db.Column(db.String(120), index=True, unique=True)
     password_hash = db.Column(db.String(128))

     # This defines a 'one-to-many' relationship. The first argument represetns
     # the 'many' side of the relationship. The `backref` argument defines the
     # name of the field that will be added to the objects of the 'many' class
     # that points back at the 'one' oobject (in this case, adding a
     # `post.author` that returns the user, given a post). The `lazy` argument
     # is... TBD.
     posts = db.relationship("Post", backref="author", lazy="dynamic")

     def __repr__(self):
        """How objects of this class are printed."""
        return "<User %s>" % self.username

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

