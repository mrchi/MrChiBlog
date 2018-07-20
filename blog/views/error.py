# coding=utf-8

from flask import Blueprint, render_template, g

bp_error = Blueprint("error", __name__)


@bp_error.app_errorhandler(400)
def http_400(e):
    if getattr(g, "bad_request_tip", None):
        tip = f"嗷嗷，请求参数 \"{g.bad_request_tip}\" 好像不太对呢 (・-・*)"  # noqa
    else:
        tip = "嗷嗷，BAD REQUEST，请检查请求参数 (・-・*)"
    return render_template("error.html", code=400, tip=tip), 400


@bp_error.app_errorhandler(403)
def http_403(e):
    tip = "抱歉，你没有权限访问这个页面 ╮(╯_╰)╭"
    return render_template("error.html", code=403, tip=tip), 403


@bp_error.app_errorhandler(404)
def http_404(e):
    tip = "诶，你来到了没有知识存在的荒原 (๑•́ ₃ •̀๑)"
    return render_template("error.html", code=404, tip=tip), 404


@bp_error.app_errorhandler(500)
def http_500(e):
    tip = "哎呀，服务器提出了一个问题 ಠ_ಠ"
    return render_template("error.html", code=500, tip=tip), 500
