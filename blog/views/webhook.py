# coding=utf-8

from flask import Blueprint, jsonify, request, current_app, g, abort

from blog.libs import CodingSignature
from blog.tasks.update import update_posts
from .common import check_args

bp_webhook = Blueprint("webhook", __name__, url_prefix="/webhook")


@bp_webhook.errorhandler(400)
def http_400(e):
    errmsg = "invalid argument"
    if getattr(g, "bad_request_tip", None):
        errmsg += f" '{g.bad_request_tip}'"     # noqa
    return jsonify(dict(success=False, errmsg=errmsg)), 400


@bp_webhook.errorhandler(403)
def http_403(e):
    return jsonify(dict(success=False, errmsg="签名验证失败")), 403


@bp_webhook.route("/coding", methods=["POST"])
@check_args("ref:str?", "before:str?", "after:str?")
def coding_webhook():
    # 鉴权
    is_ok = CodingSignature.check_webhook_signature(
        current_app.config["WEBHOOK_TOKEN"],
        request.data,
        request.headers.get("X-Coding-Signature", ""),
    )
    if not is_ok:
        abort(403)

    event = request.headers.get("X-Coding-Event", "ping")

    # 响应 push 事件
    if event == "push":
        diff_info = {
            "ref": g.args.get("ref"),
            "before": g.args.get("before"),
            "after": g.args.get("after"),
        }
        update_posts.queue(diff_info)
    # 响应 ping 事件
    elif event == "ping":
        pass

    return jsonify(dict(success=True))
