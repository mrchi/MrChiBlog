# coding=utf-8

from .tasks import celery_update

celery_apps = [celery_update]


def init_app(app):
    """
    重写 Celery App 的 Task 类，让 Celery 任务能在 Flask 上下文中执行，
    同时把 Celery App 绑定到 Flask App 上。
    """
    app.celery_apps = {}

    for celery_app in celery_apps:

        class ContextTask(celery_app.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        celery_app.Task = ContextTask

        name = celery_app.main
        if name in app.celery_apps:
            raise NameError(f"Celery app name '{name}' is repeated.")   # noqa
        app.celery_apps[name] = celery_app
