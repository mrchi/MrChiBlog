# coding=utf-8

from datetime import datetime

from flask import current_app

from . import rq
from blog.models import db, redis, Post, User, Category, Label, md_converter
from blog.libs.repo import PostRepo


@rq.job("update", timeout=180)
def update_posts(diff_info, update_all=False):
    """添加或修改文章"""
    repo = PostRepo(
        current_app.config["REPO_DIR"],
        current_app.config["REPO_SSHKEY"],
        current_app.config["REPO_BRANCH"],
    )

    if update_all:
        updated_blobs, removed_blobs = repo.get_all_posts()
    else:
        updated_blobs, removed_blobs = repo.get_diff_posts(
            ref=diff_info['ref'],
            before_sha=diff_info['before'],
            after_sha=diff_info['after'],
        )

    # 更新文章
    updated_paths = {i.path for i in updated_blobs}
    updated_posts = Post.query.filter(Post.path.in_(updated_paths)).all()
    updated_posts = {i.path: i for i in updated_posts}
    for blob in updated_blobs:
        post = updated_posts.get(blob.path) or Post(path=blob.path)

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
        print(f"{blob.name} is updated.")     # noqa

    # 删除文章
    removed_paths = {i.path for i in removed_blobs}
    removed_posts = Post.query.filter(Post.path.in_(removed_paths)).all()
    removed_posts = {i.path: i for i in removed_posts}
    for blob in removed_blobs:
        post = removed_posts.get(blob.path)
        if post:
            post.status = 2
            print(f"{blob.name} is removed.")
        else:
            print(f"{blob.name} don't exist.")

    db.session.commit()

    # 在 redis 中存储最后更新时间
    redis.set("last_update_at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
