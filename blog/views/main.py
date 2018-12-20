# coding=utf-8

from flask import Blueprint, render_template, g, abort, send_from_directory, \
    current_app
from sqlalchemy import func

from blog.models import redis, md_converter, \
    Post, Category, Label, PostLabelRef
from .common import check_args

bp_main = Blueprint("main", __name__)


@bp_main.context_processor
def inject_contexts():
    """向模版中插入 categories、labels 和 statistic 变量"""
    results = Category.query \
        .join(Post) \
        .add_columns(func.count(Post.id)) \
        .filter(Post.status == 1) \
        .group_by(Category.id) \
        .order_by(func.count(Post.id).desc()) \
        .all()
    categories = [
        {"permalink": category.permalink, "name": category.name, "posts_count": count}
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
        {"permalink": label.permalink, "name": label.name, "posts_count": count}
        for (label, count) in results if count != 0
    ]

    statistic = {
        "last_update_at": redis.get("last_update_at"),
        "posts": Post.query.filter_by(status=1).count(),
        "categories": Category.query.count(),
        "labels": Label.query.count(),
    }

    return dict(
        categories=categories,
        labels=labels,
        statistic=statistic,
    )


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


@bp_main.route("/categories")
@check_args("page:?int")
def categories():
    """所有分类页面"""
    page = g.args.get("page", 1)    # 页码
    per_page = 10                   # 分页数量
    pagination = Post.query \
        .filter_by(status=1) \
        .order_by(Post.create_at.desc()) \
        .paginate(page, per_page, error_out=False)
    posts = pagination.items

    return render_template(
        "categories.html",
        posts=posts,
        pagination=pagination,
        endpoint="main.categories",
    )


@bp_main.route("/category/<string:permalink>")
@check_args("page:?int")
def category(permalink):
    """分类详情页"""
    page = g.args.get("page", 1)    # 页码
    per_page = 10                   # 分页数量
    category = Category.query.filter_by(permalink=permalink).one_or_none()
    if not category:
        abort(404)

    pagination = category.posts \
        .filter_by(status=1) \
        .order_by(Post.create_at.desc()) \
        .paginate(page, per_page, error_out=False)
    posts = pagination.items

    return render_template(
        "category.html",
        category=category,
        pagination=pagination,
        posts=posts,
        endpoint="main.category",
    )


@bp_main.route("/labels")
def labels():
    """所有标签页面"""
    return render_template("labels.html")


@bp_main.route("/label/<string:permalink>")
@check_args("page:?int")
def label(permalink):
    """标签详情页"""
    page = g.args.get("page", 1)    # 页码
    per_page = 10                   # 分页数量
    label = Label.query.filter_by(permalink=permalink).one_or_none()
    if not label:
        abort(404)

    pagination = label.posts \
        .filter_by(status=1) \
        .order_by(Post.create_at.desc()) \
        .paginate(page, per_page, error_out=False)
    posts = pagination.items

    return render_template(
        "label.html",
        label=label,
        pagination=pagination,
        posts=posts,
        endpoint="main.label",
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


@bp_main.route("/about")
def about():
    with open("README.md") as f:
        content = f.read()
    html_content = md_converter.convert(content)
    return render_template(
        "about.html",
        html_content=html_content,
    )


@bp_main.route("/robots.txt")
def robots_txt():
    return send_from_directory(current_app.static_folder, 'robots.txt')
