# coding=utf-8

import os


class Config:
    REPO_DIR = os.environ.get("REPO_DIR")
    REPO_BRANCH = "master"
    WEBHOOK_TOKEN = os.environ.get("WEBHOOK_TOKEN")

    HMAC_KEY = os.environ.get("HMAC_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI")
    REDIS_URL = os.environ.get("DEV_REDIS_URI") or "redis://127.0.0.1:6379/0"
    WHOOSH_BASE = os.environ.get("DEV_WHOOSH_BASE") or "dev_whoosh_idx"
    DINGTALK_ROBOT_TOKEN = os.environ.get("DEV_DINGTALK_TOKEN")
    RQ_REDIS_URL = os.environ.get("DEV_RQ_REDIS_URI") or "redis://127.0.0.1:6379/1"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")
    REDIS_URL = os.environ.get("TEST_REDIS_URI")
    WHOOSH_BASE = os.environ.get("TEST_WHOOSH_BASE") or "test_whoosh_idx"
    DINGTALK_ROBOT_TOKEN = os.environ.get("TEST_DINGTALK_TOKEN")
    RQ_REDIS_URL = os.environ.get("TEST_RQ_REDIS_URI")
    RQ_ASYNC = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATABASE_URI")
    REDIS_URL = os.environ.get("PROD_REDIS_URI")
    WHOOSH_BASE = os.environ.get("PROD_WHOOSH_BASE") or "prod_whoosh_idx"
    DINGTALK_ROBOT_TOKEN = os.environ.get("PROD_DINGTALK_TOKEN")
    RQ_REDIS_URL = os.environ.get("PROD_RQ_REDIS_URI")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
