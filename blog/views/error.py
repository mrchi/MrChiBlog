# coding=utf-8

from flask import Blueprint, render_template

bp_error = Blueprint("error", __name__)


@bp_error.app_errorhandler(404)
def http_404(e):
    tip = "你来到了没有知识存在的荒原 (๑•́ ₃ •̀๑)"
    return render_template("error.html", code=404, tip=tip), 404


@bp_error.app_errorhandler(500)
def http_500(e):
    tip = "服务器提出了一个问题 ╮(╯_╰)╭"
    return render_template("error.html", code=500, tip=tip), 500


@bp_error.app_errorhandler(403)
def http_403(e):
    tip = "抱歉，你没有权限访问这个页面 ಠ_ಠ"
    return render_template("error.html", code=403, tip=tip), 403
