# coding=utf-8

import os


class Config:
    OWNER = os.environ.get("OWNER")
    PROJECT = os.environ.get("PROJECT")
    ROOTDIR = os.environ.get("ROOTDIR")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    WEBHOOK_TOKEN = os.environ.get("WEBHOOK_TOKEN")

    HMAC_KEY = os.environ.get("HMAC_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI") or \
        "sqlite:///./data-dev.sqlite"
    REDIS_URL = os.environ.get("DEV_REDIS_URI") or "redis://127.0.0.1:6379/0"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI") or \
        "sqlite:///./data-test.sqlite"
    REDIS_URL = os.environ.get("TEST_REDIS_URI")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATABASE_URI") or \
        "sqlite:///./data-prod.sqlite"
    REDIS_URL = os.environ.get("PROD_REDIS_URI")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
