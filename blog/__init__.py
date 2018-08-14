# coding=utf-8

from flask import Flask
import flask_whooshalchemyplus
import jieba

from blog import views
from blog import celerys
from blog.models import db, redis


def create_app(config_obj):
    """factory function"""
    app = Flask(__name__)
    app.config.from_object(config_obj)

    db.init_app(app)
    flask_whooshalchemyplus.init_app(app)
    redis.init_app(app)

    views.init_app(app)
    celerys.init_app(app)

    jieba.initialize()

    return app
