# coding=utf-8

from flask import Blueprint

bp_webhook = Blueprint("webhook", __name__, url_prefix="/webhook")

from blog.webhook import views
