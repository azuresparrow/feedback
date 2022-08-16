
"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Establishes the connection"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users can create feedback"""
    __tablename__ = 'users'

    username = db.Column(db.String(20), 
                   primary_key=True)
    
    password = db.Column(db.Text,
                    nullable=False)

    email= db.Column(db.String(50),
                    nullable=False)

    first_name = db.Column(db.String(30),
                    nullable=False)
        
    last_name = db.Column(db.String(30),
                    nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, username, pwd, email, first, last):
        """Create a user and hash their password"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first, last_name=last)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate the user, that they exist and their password is correct"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
    
    @classmethod
    def username_taken(cls, username):
        """returns if the username is taken"""
        user = User.query.filter_by(username=username).first()
        if user:
            return True
        return False


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(100),
                    nullable=False)

    content = db.Column(db.Text,
                    nullable=False)

    username = db.Column(db.String(20),
                    db.ForeignKey('users.username', ondelete='CASCADE'))
