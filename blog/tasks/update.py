# coding=utf-8

from flask import current_app

from . import rq
from blog.models import db, Post, User, Category, Label, md_converter
from blog.libs.repo import PostRepo


@rq.job("update", timeout=60)
def remove_posts(removed_paths):
    """删除文章"""
    removed_paths = set(removed_paths)
    posts = Post.query.filter(Post.path.in_(removed_paths)).all()

    # 删除存在的文章
    for post in posts:
        post.status = 2
        removed_paths.remove(post.path)
        print(f"{post.title} is removed.")
    # 不存在的文章
    for path in removed_paths:
        print(f"{path} don't exist.")

    db.session.commit()


@rq.job("update", timeout=180)
def update_posts(updated_blobs, update_all=False):
    """添加或修改文章"""
    repo = PostRepo(
        current_app.config["REPO_DIR"],
        current_app.config["REPO_SSHKEY"],
        current_app.config["REPO_BRANCH"],
    )
    # 是否全量更新
    if update_all:
        updated_blobs = repo.get_post_list()
    else:
        updated_blobs = set(updated_blobs)

    for blob in updated_blobs:
        post = Post.query.filter_by(path=blob.path).one_or_none() \
            or Post(path=blob.path)

        # 拉取文章信息
        data = repo.get_post_detail(blob)

        # 获取 Author 对象
        author_email = data["author"]["email"]
        author = User.query.filter_by(email=author_email).one_or_none() \
            or User(email=author_email)
        author.name = data["author"]["name"]

        # 获取文章的 Meta-data 数据
        content = data["content"]
        html_content = md_converter.convert(content)
        meta_data = md_converter.Meta

        # 获取 Category 对象
        category = meta_data["category"][0]
        category = Category.query.filter_by(name=category).one_or_none() \
            or Category(name=category)

        # 获取 Label 对象列表
        labels = set()
        for label in meta_data["labels"]:
            label = Label.query.filter_by(name=label).one_or_none() \
                or Label(name=label)
            labels.add(label)

        # 更新文章
        post.title = data["title"]
        post.content = content
        post.html_content = html_content
        post.update_at = data["update_time"]
        post.create_at = data["create_time"]
        post.author = author
        post.category = category
        post.labels = labels

        db.session.add(post)
        print(f"{post.title} is updated.")     # noqa

        db.session.commit()
