# coding=utf-8

import uuid
from urllib.parse import urljoin

from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    avatar = db.Column(db.String(256))
    permalink = db.Column(db.String(128), unique=True, nullable=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    @property
    def avatar_url(self):
        return urljoin(current_app.config["CODING_DOMAIN"], self.avatar)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.permalink is None:
            self.permalink = uuid.uuid4().hex


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False, default="")
    html_content = db.Column(db.Text, nullable=False, default="")
    last_update = db.Column(db.DateTime, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
