# coding=utf-8

from flask import Blueprint, render_template, g, abort
from sqlalchemy import func

from blog.models import Post, Category, Label, PostLabelRef
from .common import check_args

bp_main = Blueprint("main", __name__)


@bp_main.context_processor
def inject_contexts():
    """向模版中插入 categories 和 labels 变量"""
    results = Category.query \
        .join(Post) \
        .add_columns(func.count(Post.id)) \
        .filter(Post.status == 1) \
        .group_by(Category.id) \
        .order_by(func.count(Post.id).desc()) \
        .all()
    categories = [
        {"id": category.id, "name": category.name, "posts_count": count}
        for (category, count) in results if count != 0
    ]

    results = Label.query \
        .join(PostLabelRef) \
        .join(Post) \
        .add_columns(func.count(Post.id)) \
        .filter(Post.status == 1) \
        .group_by(Label.id) \
        .order_by(func.count(Post.id).desc()) \
        .all()
    labels = [
        {"id": label.id, "name": label.name, "posts_count": count}
        for (label, count) in results if count != 0
    ]

    return dict(categories=categories, labels=labels)


@bp_main.route("/")
@check_args("page:?int")
def index():
    """主页"""
    page = g.args.get("page", 1)    # 页码
    per_page = 10                   # 分页数量
    pagination = Post.query \
        .filter_by(status=1) \
        .order_by(Post.create_at.desc()) \
        .paginate(page, per_page, error_out=False)
    posts = pagination.items

    return render_template(
        "index.html",
        posts=posts,
        pagination=pagination,
        endpoint="main.index",
    )


@bp_main.route("/p/<string:permalink>")
def post(permalink):
    """文章内容页"""
    post = Post.query.filter_by(status=1, permalink=permalink).one_or_none()
    if not post:
        abort(404)

    return render_template(
        "post.html",
        post=post,
    )


@bp_main.route("/search")
@check_args("q:?str", "page:?int")
def search():
    """全文搜索文章标题和内容"""
    keyword = g.args.get("q", "").strip()
    page = g.args.get("page", 1)
    per_page = 10
    pagination = Post.query \
        .whoosh_search(keyword) \
        .filter_by(status=1) \
        .paginate(page, per_page, error_out=False)

    posts = pagination.items
    return render_template(
        "search.html",
        keyword=keyword,
        posts=posts,
        pagination=pagination,
        endpoint="main.search",
    )
