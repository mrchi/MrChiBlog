# coding=utf-8

from celery import Celery

from . import celeryconfig
from blog.libs.apis import DingTalkRobot

celery_notify = Celery("celery_notify")
celery_notify.config_from_object(celeryconfig)
celery_notify.conf.update(task_default_queue="notify_queue")


@celery_notify.task(shared=False)
def send_500_notify():
    print(DingTalkRobot)
    print('test')
