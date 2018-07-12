# coding=utf-8

from flask import jsonify, request, current_app

from blog.webhook import bp_webhook
from blog.libs.coding import CodingSignature


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
    return jsonify(dict(success=True))
