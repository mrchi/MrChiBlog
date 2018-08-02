# coding=utf-8

from flask import Blueprint, jsonify, request, current_app, g

from blog.libs.coding import CodingSignature
from blog.celerys.update_tasks import remove_posts, update_posts
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
@check_args("commits:list?", "head_commit:?dict")
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
    # 响应 ping 事件
    if event == "ping":
        return jsonify(dict(success=True))
    # 获取更新列表
    commits = g.args.get("commits") or [g.args["head_commit"]]
    paths = {}
    for commit in reversed(commits):
        for type_ in ("added", "modified", "removed"):
            paths.update({file: type_ for file in commit[type_]})
    removed_paths = [i for i in paths if paths[i] == "removed"]
    updated_paths = [i for i in paths if paths[i] in ("added", "modified")]

    # Celery任务执行
    remove_posts.delay(removed_paths)
    update_posts.delay(updated_paths)

    return jsonify(dict(success=True))
