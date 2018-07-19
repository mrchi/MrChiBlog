# coding=utf-8

from datetime import datetime

from celery import Celery
from flask import current_app

from . import celeryconfig
from blog.models import db, Post, User
from blog.libs.coding import CodingPost

celery_update = Celery("celery_update")
celery_update.config_from_object(celeryconfig)


@celery_update.task(shared=False)
def remove_posts(removed_paths):
    """删除文章"""
    removed_paths = set(removed_paths)
    posts = Post.query.filter(Post.coding_path.in_(removed_paths)).all()

    # 删除存在的文章
    for post in posts:
        post.status = 2
        removed_paths.remove(post.coding_path)
        print(f"{post.title} is removed.")      # noqa
    # 不存在的文章
    for path in removed_paths:
        print(f"{path} don't exist.")       # noqa

    db.session.commit()


@celery_update.task(shared=False)
def update_posts(updated_paths, update_all=False):
    """添加或修改文章"""
    coding = CodingPost(
        current_app.config["ACCESS_TOKEN"],
        current_app.config["OWNER"],
        current_app.config["PROJECT"],
        current_app.config["ROOTDIR"],
    )
    # 是否全量更新
    if update_all:
        updated_paths = coding.get_all_paths()
    updated_paths = set(updated_paths)

    # 查询已存在文章
    posts = Post.query.filter(Post.coding_path.in_(updated_paths)).all()
    posts = {i.coding_path: i for i in posts}
    for path in updated_paths:
        post = posts.get(path) or Post(coding_path=path)
        # 获取文章内容
        data = coding.get_file_content(path)
        # 获取 Author 对象
        author = User.query.filter_by(username=data["author"]).one_or_none() \
            or User(username=data["author"])
        # 更新文章
        post.title = data["title"]
        post.content = data["content"]
        post.last_update = datetime.fromtimestamp(data["timestamp"]/1000)
        post.author = author

        db.session.add(author)
        db.session.add(post)
        print(f"{post.title} is updated.")     # noqa

    db.session.commit()
