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
    return dict(db=db)
