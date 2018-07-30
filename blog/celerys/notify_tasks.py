# coding=utf-8

from datetime import datetime

from flask import current_app
from celery import Celery

from . import celeryconfig
from blog.models import redis
from blog.libs.apis import DingTalkRobot

celery_notify = Celery("celery_notify")
celery_notify.config_from_object(celeryconfig)
celery_notify.conf.update(task_default_queue="notify_queue")


@celery_notify.task(shared=False)
def send_500_notify(url, errmsg):
    """发送HTTP 500异常通知给管理员"""
    robot = DingTalkRobot(current_app.config["DINGTALK_ROBOT_TOKEN"])
    title = "博客500通知"
    time = datetime.now().strftime("%c")
    text = "\n\n".join([
        f"#### {title}",    # noqa
        f"> 出错地址：{url}",        # noqa
        f"> 出错类型：{errmsg}",     # noqa
        f"###### {time}",   # noqa
    ])
    robot.send_markdown_msg(title, text)
