# coding=utf-8

__author__ = "Invoker"

import unittest
from source.base import APIBase


class TestAPIBase(unittest.TestCase):
    def setUp(self):
        self.base = APIBase()
        self.base.set_connection_timeout(15)
        self.base.set_socket_timeout(15)

    def test_get(self):
        url = "https://httpbin.org/get"
        params = dict(foo="bar")
        resp = self.base._get(url, params=params)

        self.assertEqual(resp["url"], "https://httpbin.org/get?foo=bar")
        self.assertEqual(resp["args"], params)

    def test_post_json(self):
        url = "https://httpbin.org/post"
        data = dict(foo="bar")
        resp = self.base._post(url, json=data)

        self.assertEqual(resp["url"], url)
        self.assertEqual(resp["data"], '{"foo": "bar"}')
        self.assertEqual(resp["headers"]["Content-Type"], "application/json")

    def test_post_form(self):
        url = "https://httpbin.org/post"
        data = dict(foo="bar")
        resp = self.base._post(url, data=data)

        self.assertEqual(resp["url"], url)
        self.assertEqual(resp["form"], data)
        self.assertEqual(
            resp["headers"]["Content-Type"],
            "application/x-www-form-urlencoded"
        )

    def test_put(self):
        url = "https://httpbin.org/put"
        data = dict(foo="bar")
        resp = self.base._put(url, json=data)

        self.assertEqual(resp["url"], url)
        self.assertEqual(resp["data"], '{"foo": "bar"}')
        self.assertEqual(resp["headers"]["Content-Type"], "application/json")

    def test_delete(self):
        url = "https://httpbin.org/delete"
        resp = self.base._delete(url)

        self.assertEqual(resp["url"], url)

    def test_error_sdk001(self):
        url = "https://httpbin.org/delay/3"
        self.base.set_connection_timeout(1)
        self.base.set_socket_timeout(1)
        resp = self.base._get(url)

        self.assertEqual(resp["errcode"], "sdk001")

    def test_error_sdk002(self):
        url = "https://httpbin.org/html"
        resp = self.base._get(url)

        self.assertEqual(resp["errcode"], "sdk002")
