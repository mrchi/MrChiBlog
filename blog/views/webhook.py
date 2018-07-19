# coding=utf-8

from flask import Blueprint, jsonify, request, current_app

from blog.libs.coding import CodingSignature
from blog.celerys.tasks import remove_posts, update_posts

bp_webhook = Blueprint("webhook", __name__, url_prefix="/webhook")


@bp_webhook.route("/coding", methods=["GET", "POST"])
def coding_webhook():
    # 鉴权
    is_ok = CodingSignature.check_webhook_signature(
        current_app.config["WEBHOOK_TOKEN"],
        request.data,
        request.headers.get("X-Coding-Signature", ""),
    )
    if not is_ok:
        return jsonify(dict(success=False, errmsg="签名验证失败")), 403

    event = request.headers.get("X-Coding-Event", "ping")
    # 响应 ping 事件
    if event == "ping":
        return jsonify(dict(success=True))
    # 获取更新列表
    data = request.json
    paths = {}
    commits = data.get("commits") or [data["head_commit"]]
    for commit in reversed(commits):
        for type_ in ("added", "modified", "removed"):
            paths.update({file: type_ for file in commit[type_]})
    removed_paths = [i for i in paths if paths[i] == "removed"]
    updated_paths = [i for i in paths if paths[i] in ("added", "modified")]

    # Celery任务执行
    remove_posts.delay(removed_paths)
    update_posts.delay(updated_paths)

    return jsonify(dict(success=True))
