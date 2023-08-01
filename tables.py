from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
db = SQLAlchemy()


user_cafes = db.Table("user_cafes",
                      db.Column("user_id",db.Integer, db.ForeignKey("users.id")),
                      db.Column("cafe_id", db.Integer, db.ForeignKey("cafe.id")))
class User(db.Model, UserMixin, Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250))
    email = db.Column(db.String(250))
    password = db.Column(db.String(250))
    liked_cafes = db.relationship("CoffeeShop",secondary=user_cafes, backref="liked_cafes", lazy=True)
    comments = db.relationship("Comment", backref="user_comments")

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
class CoffeeShop(db.Model, UserMixin, Base):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(250))
    map_url = db.Column(db.String(250))
    location = db.Column(db.String(500))
    name = db.Column(db.String(250))
    has_sockets = db.Column(db.Boolean)
    has_toilet = db.Column(db.Boolean)
    has_wifi = db.Column(db.Boolean)
    can_take_calls = db.Column(db.Boolean)
    seats = db.Column(db.String)
    coffee_price = db.Column(db.String)
    liked_by = db.relationship("User", secondary=user_cafes, backref="selected")
    comments = db.relationship("Comment", backref="cafe_comment")

    def __init__(self, liked_by=None):
        self.liked_by = liked_by


class Comment(db.Model, UserMixin):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    date = db.Column(db.DateTime)
    user = db.Column(db.Integer, db.ForeignKey("users.id"), name="user_id")
    cafe = db.Column(db.Integer, db.ForeignKey("cafe.id"), name="cafe_id",)

    def __init__(self, content, user, cafe, date):
        self.content = content
        self.user = user
        self.cafe = cafe
        self.date = date



