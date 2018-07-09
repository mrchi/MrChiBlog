# coding=utf-8

from blog.main import bp_main


@bp_main.route("/")
def index():
    return "hello, world!"
