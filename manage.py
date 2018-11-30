#!/usr/bin/env python3
# coding=utf-8

import os
from datetime import datetime

import click

from blog import create_app
from blog.models import db, redis, Post, User, Category, Label, PostLabelRef
from blog.tasks.update import update_posts
from config import config

app = create_app(config[os.getenv('FLASK_ENV') or 'default'])


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        redis=redis,
        Post=Post,
        User=User,
        Category=Category,
        Label=Label,
        PostLabelRef=PostLabelRef,
    )


@app.cli.command(help="Update all posts.")
@click.option('--dropdb', is_flag=True, help="Drop and rebuild database.")
def deploy(dropdb):
    if dropdb:
        db.drop_all()
        print("Database is droped.")
    db.create_all()
    print("---------- Start update. ----------")
    update_posts([], update_all=True)
    print("----------- End update. -----------")

    # 在 redis 中存储最后更新时间
    redis.set("last_update_at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
