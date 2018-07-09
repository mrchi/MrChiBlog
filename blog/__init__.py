# coding=utf-8

from flask import Flask

from blog.models import db
from blog.main import bp_main
from blog.manage import bp_manage
from blog.webhook import bp_webhook


def create_app(config_obj):
    """factory function"""
    app = Flask(__name__)
    app.config.from_object(config_obj)

    db.init_app(app)

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_manage)
    app.register_blueprint(bp_webhook)

    return app
