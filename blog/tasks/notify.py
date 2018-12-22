# coding=utf-8

from datetime import datetime

from flask import current_app

from . import rq
from blog.libs import DingTalkRobot


@rq.job("notify", timeout=60)
def send_500_notify(url, errmsg):
    """发送HTTP 500异常通知给管理员"""
    robot = DingTalkRobot(current_app.config["DINGTALK_ROBOT_TOKEN"])
    title = "博客500通知"
    time = datetime.now().strftime("%c")
    text = "\n\n".join([
        f"#### {title}",
        f"> 出错地址：{url}",
        f"> 出错类型：{errmsg}",
        f"###### {time}",
    ])
    robot.send_markdown_msg(title, text)
