# coding=utf-8

from flask import Blueprint

bp_manage = Blueprint("manage", __name__)


@bp_manage.route("/manage")
def manage():
    return "haha"
