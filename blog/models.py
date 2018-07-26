# coding=utf-8

from urllib.parse import urljoin

from markdown import markdown
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT


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
    content = db.Column(LONGTEXT, nullable=False)
    html_content = db.Column(LONGTEXT, nullable=False, default="")
    last_update = db.Column(db.DateTime, nullable=False)
    coding_path = db.Column(db.String(256), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False, default=0)   # 0:未公开，1:公开，2:删除
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)


@db.event.listens_for(Post.content, "set")
def on_changed_md(target, value, oldvalue, initiator):
    """转换 markdown 为 html"""
    extensions = [
        "markdown.extensions.fenced_code",      # 代码块
        "markdown.extensions.codehilite",       # 代码块代码高亮
        "markdown.extensions.sane_lists",       # 非混合列表
        "markdown.extensions.smarty",           # 自动转译字符的html表示形式
        "markdown.extensions.tables",           # 表格
        "markdown.extensions.toc",              # 目录支持
    ]
    extension_configs = {
        "markdown.extensions.codehilite": {"linenums": False},  # 不显示行号
    }
    target.html_content = markdown(
        value,
        output_format="html5",
        extensions=extensions,
        extension_configs=extension_configs,
        strip=True,
    )
