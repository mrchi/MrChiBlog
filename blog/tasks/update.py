# coding=utf-8

from datetime import datetime

from flask import current_app

from . import rq
from blog.models import db, Post, User, Category, Label, md_converter
from blog.libs.coding import CodingPost


@rq.job("update", timeout=60)
def remove_posts(removed_paths):
    """删除文章"""
    removed_paths = set(removed_paths)
    posts = Post.query.filter(Post.coding_path.in_(removed_paths)).all()

    # 删除存在的文章
    for post in posts:
        post.status = 2
        removed_paths.remove(post.coding_path)
        print(f"{post.title} is removed.")
    # 不存在的文章
    for path in removed_paths:
        print(f"{path} don't exist.")

    db.session.commit()


@rq.job("update", timeout=180)
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

        # 拉取文章信息
        data = coding.get_file_content(path)

        # 获取 Author 对象
        author_name = data["author"]["name"]
        author = User.query.filter_by(username=author_name).one_or_none() \
            or User(username=author_name)
        author.avatar = data["author"]["avatar"]

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

        # 获取创建时间
        create_at = meta_data["create_at"][0]

        # 更新文章
        post.title = data["title"]
        post.content = content
        post.html_content = html_content
        post.update_at = datetime.fromtimestamp(data["timestamp"]/1000)
        post.create_at = datetime.strptime(create_at, "%Y-%m-%d %H:%M:%S")
        post.author = author
        post.category = category
        post.labels = labels

        db.session.add(post)
        print(f"{post.title} is updated.")     # noqa

    db.session.commit()
