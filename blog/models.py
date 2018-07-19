# coding=utf-8

import uuid
from urllib.parse import urljoin

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    avatar = db.Column(db.String(256))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    @property
    def avatar_url(self):
        return urljoin("https://coding.net", self.avatar)


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    html_content = db.Column(db.Text, nullable=False, default="")
    last_update = db.Column(db.DateTime, nullable=False)
    coding_path = db.Column(db.String(256), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False, default=0)   # 0:未公开，1:公开，2:删除
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
