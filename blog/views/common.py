# coding=utf-8

import functools

from flask import request, g, abort

__all__ = ["check_args"]

_allowed_types = ("int", "str", "bool", "list", "tuple", "dict", "set")


# 参数检查装饰器，传参格式 "arg_name:[?]arg_type"，?代表可选参数
def check_args(*expacted_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            g.args = {}
            request_args = _obtain_args()
            for arg in expacted_args:
                # 解析传参
                optional = True if "?" in arg else False
                arg_name, arg_type = arg.replace("?", "").split(":")
                # 检查 arg_type
                if arg_type not in _allowed_types:
                    raise ValueError("arg_type only support {types}.".format(
                        types=", ".join(_allowed_types),
                    ))
                # 如果 arg_value 存在且类型正确，存入 g.args 中，否则 correct=False
                arg_value = request_args.get(arg_name)
                if arg_value is not None:
                    try:
                        arg_value = eval(arg_type)(arg_value)
                        g.args[arg_name] = arg_value
                        correct = True
                    except (ValueError, TypeError):
                        correct = False
                else:
                    correct = False
                # 如果不是可选参数并且参数检查失败，抛出 HTTP 400 错误
                if not optional and not correct:
                    g.bad_request_tip = arg_name
                    abort(400)
            return func(*args, **kw)
        return wrapper
    return decorator


def _obtain_args():
    """
    获取请求参数，参数重复时只取一个。

    GET请求：获取 URL 参数。
    POST请求：参数优先级：JSON参数 > FORM参数 > URL参数。
    """
    if request.method == "GET":
        args = _obtain_get_args()
    elif request.method in ("POST", "PUT"):
        args = {}
        args.update(_obtain_get_args())
        args.update(_obtain_form_args())
        args.update(_obtain_json_args())
    else:
        args = {}
    return args


def _obtain_get_args():
    return request.args.to_dict(flat=True) or {}


def _obtain_json_args():
    return request.get_json(silent=True) or {}


def _obtain_form_args():
    return request.form.to_dict(flat=True) or {}
