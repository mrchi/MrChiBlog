#!/usr/bin/env python3
# coding=utf-8

import os

from flask_migrate import Migrate

from blog import create_app, db
from config import config

app = create_app(config[os.getenv('FLASK_ENV') or 'default'])
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, **app.celery_apps)


for name, celery_app in app.celery_apps.items():
    if name in globals():
        raise NameError(f"Celery app name '{name}' is repeated.")   # noqa
    globals()[name] = celery_app
