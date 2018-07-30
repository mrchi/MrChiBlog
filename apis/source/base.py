# coding=utf-8

__author__ = "Invoker"

from json import JSONDecodeError
from functools import partialmethod

import requests
from requests.exceptions import ReadTimeout, ConnectTimeout


class APIBase(object):
    """ 自定义web请求类，封装requests """
    def __init__(self, req=None):
        self._client = req or requests
        self.__connect_timeout = 5.0
        self.__socket_timeout = 5.0
        self.__proxies = {}

    def set_connection_timeout(self, second):
        """设置请求超时时间，单位秒"""
        self.__connect_timeout = second

    def set_socket_timeout(self, second):
        """设置响应超时时间，单位秒"""
        self.__socket_timeout = second

    def set_proxies(self, proxies):
        """设置代理"""
        self.__proxies = proxies

    def _request(self, method, url, params=None, data=None, json=None, **kw):
        """自定义请求"""
        try:
            resp = self._client.request(
                method.upper().strip(),
                url,
                params=params,
                data=data,
                json=json,
                timeout=(self.__connect_timeout, self.__socket_timeout),
                proxies=self.__proxies,
                **kw
            )
            data = resp.json()
        except (ReadTimeout, ConnectTimeout):
            return {
                "errcode": "sdk001",
                "errmsg": "connection or read data timeout",
            }
        except JSONDecodeError:
            return {
                "errcode": "sdk002",
                "errmsg": "invalid json data",
            }
        return data

    _get = partialmethod(_request, "GET")
    _post = partialmethod(_request, "POST")
    _put = partialmethod(_request, "PUT")
    _delete = partialmethod(_request, "DELETE")
