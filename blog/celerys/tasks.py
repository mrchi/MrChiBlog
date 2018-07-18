# coding=utf-8

from celery import Celery
from . import celeryconfig


celery_update = Celery("celery_update")
celery_update.config_from_object(celeryconfig)


@celery_update.task(shared=False)
def update_posts():
    print("haha")
