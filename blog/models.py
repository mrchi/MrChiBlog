# coding=utf-8

import hmac

from markdown import Markdown
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from sqlalchemy.dialects.mysql import LONGTEXT
from jieba.analyse import ChineseAnalyzer


db = SQLAlchemy()
redis = FlaskRedis()

md_converter = Markdown(
    output_format="html5",
    extensions=[
        "markdown.extensions.fenced_code",      # 代码块
        "markdown.extensions.codehilite",       # 代码块代码高亮
        "markdown.extensions.sane_lists",       # 非混合列表
        "markdown.extensions.smarty",           # 自动转译字符的 html 表示形式
        "markdown.extensions.tables",           # 表格
        "markdown.extensions.toc",              # 目录支持
        "markdown.extensions.meta",             # Meta-data 支持
    ],
    extension_configs={
        "markdown.extensions.codehilite": {"linenums": False},  # 不显示行号
    },
    strip=True,
)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64), default="")
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return "<User %r>" % self.email


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    posts = db.relationship("Post", backref="category", lazy="dynamic")

    def __repr__(self):
        return "<Category %r>" % self.name


class Label(db.Model):
    __tablename__ = "label"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    posts = db.relationship(
        "Post",
        secondary="post_label_ref",
        backref=db.backref("labels", lazy="dynamic"),
        lazy="dynamic",
    )

    def __repr__(self):
        return "<Label %r>" % self.name


class Post(db.Model):
    __tablename__ = "post"
    __searchable__ = ["title", "content"]
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    content = db.Column(LONGTEXT, nullable=False)
    html_content = db.Column(LONGTEXT, nullable=False, default="")
    create_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime, nullable=False)
    coding_path = db.Column(db.String(256), nullable=False, unique=True)
    permalink = db.Column(db.String(128), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False, default=1)   # 1:公开，2:删除
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)

    def __repr__(self):
        return "<Post %r>" % self.title

    def __init__(self, **kw):
        super(Post, self).__init__(**kw)
        if self.coding_path is not None and self.permalink is None:
            self.permalink = hmac.new(
                current_app.config["HMAC_KEY"].encode("utf-8"),
                self.coding_path.encode("utf-8"),
                "md5",
            ).hexdigest()


class PostLabelRef(db.Model):
    __tablename__ = "post_label_ref"
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id), primary_key=True)
    label_id = db.Column(db.Integer, db.ForeignKey(Label.id), primary_key=True)


@db.event.listens_for(Post.content, "set")
def on_changed_md(target, value, oldvalue, initiator):
    """转换 markdown 为 html"""
    target.html_content = md_converter.convert(value)
