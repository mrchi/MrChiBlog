# coding=utf-8

from .main import bp_main
from .manage import bp_manage
from .webhook import bp_webhook
from .error import bp_error


def init_app(app):
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_manage)
    app.register_blueprint(bp_webhook)
    app.register_blueprint(bp_error)
