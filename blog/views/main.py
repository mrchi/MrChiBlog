# coding=utf-8

from flask import Blueprint

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
def index():
    return "hello, world!"
