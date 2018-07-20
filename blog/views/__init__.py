# coding=utf-8

from blog.views.main import bp_main
from blog.views.manage import bp_manage
from blog.views.webhook import bp_webhook
from blog.views.error import bp_error


def init_app(app):
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_manage)
    app.register_blueprint(bp_webhook)
    app.register_blueprint(bp_error)
