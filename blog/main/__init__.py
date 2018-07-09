# coding=utf-8

from flask import Blueprint

bp_main = Blueprint("main", __name__)

from blog.main import views, errors
