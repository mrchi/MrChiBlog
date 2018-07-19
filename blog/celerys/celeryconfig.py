# coding=utf-8

import os

broker_url = os.environ.get("CELERY_BROKER_URL")
result_backend = os.environ.get("CELERY_RESULT_BACKED")
task_default_queue = "update_queue"
timezone = "Asia/Shanghai"
task_soft_time_limit = 60
