# coding=utf-8

from flask import Blueprint, render_template, g, abort

from blog.models import Post
from .common import check_args

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
@check_args("page:?int")
def index():
    """主页"""
    page = g.args.get("page", 1)    # 页码
    per_page = 10                   # 分页数量
    pagination = Post.query \
        .filter_by(status=1) \
        .order_by(Post.last_update.desc()) \
        .paginate(page, per_page, error_out=False)

    posts = pagination.items

    return render_template(
        "index.html",
        posts=posts,
        pagination=pagination,
        endpoint="main.index",
    )


@bp_main.route("/p/<string:permalink>")
def content(permalink):
    """文章内容页"""
    post = Post.query.filter_by(status=1, permalink=permalink).one_or_none()
    if not post:
        abort(404)

    return render_template(
        "post.html",
        post=post,
    )
