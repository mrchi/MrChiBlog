# coding=utf-8

__author__ = "Invoker"

import urllib.parse

from .base import APIBase


class WxOauth2(APIBase):
    """
    微信Oauth2.0授权

    包括 开放平台网站应用授权 和 公众平台微信内网页授权
    """

    __webapp_oauth_url = \
        "https://open.weixin.qq.com/connect/qrconnect#wechat_redirect"

    __mp_oauth_url = \
        "https://open.weixin.qq.com/connect/oauth2/authorize#wechat_redirect"

    __access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"

    __refresh_token_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"

    __check_token_url = "https://api.weixin.qq.com/sns/auth"

    __userinfo_url = "https://api.weixin.qq.com/sns/userinfo"

    def __init__(self, appid, appsecret, req=None):
        self._appid = appid.strip()
        self._appsecret = appsecret.strip()
        super().__init__(rep=req)

    def gen_webapp_oauth_url(self, redirect_uri, state=None):
        """生成微信开放平台网站应用授权链接，跳转链接后用户可扫码登录"""
        state = state or ""
        params = {
            "appid": self._appid,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "snsapi_login",
            "state": state,
        }
        split_result = list(urllib.parse.urlsplit(self.__webapp_oauth_url))
        split_result[3] = urllib.parse.urlencode(params)
        return urllib.parse.urlunsplit(split_result)

    def gen_webapp_embedded_qrcode_params(self, redirect_uri, state=None):
        """
        生成 网页中嵌入的微信登录二维码 需要的参数。

        这种方式不需要跳转到微信域名，更加友好，通过 JS 可定义样式。
        """
        state = state or ""
        params = {
            "appid": self._appid,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "snsapi_login",
            "state": state,
        }
        return params

    def gen_mp_oauth_url(self, redirect_uri, state=None, silent_oauth=False):
        """生成微信网页授权链接，在微信浏览器中，引导用户访问后获得用户授权"""
        state = state or ""
        scope = "snsapi_base" if silent_oauth else "snsapi_userinfo"
        params = {
            "appid": self._appid,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "state": state,
        }
        split_result = list(urllib.parse.urlsplit(self.__mp_oauth_url))
        split_result[3] = urllib.parse.urlencode(params)
        return urllib.parse.urlunsplit(split_result)

    def get_access_token(self, code):
        """通过用户授权后，用得到的 code 换取 access_token 和 openid"""
        params = {
            "appid": self._appid,
            "secret": self._appsecret,
            "code": code,
            "grant_type": "authorization_code",
        }
        return self._get(self.__access_token_url, params=params)

    def renew_access_token(self, refresh_token):
        """
        使用 refresh_token 刷新 access_token 有效期，也会得到新的 refresh_token。

        1. 若access_token已超时，那么会获取一个新的access_token，新的超时时间；
        2. 若access_token未超时，那么不会改变access_token，但超时时间会刷新，相当于续期。

        refresh_token 拥有较长的有效期（30天），当 refresh_token 失效的后，需要用户重新
        授权，所以，请开发者在refresh_token即将过期时（如第29天时），进行定时的自动刷新并保
        存好它。
        """
        params = {
            "appid": self._appid,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        return self._get(self.__refresh_token_url, params=params)

    def check_access_tokene(self, access_token, openid):
        """检查 access_token 是否有效"""
        params = {
            "access_token": access_token,
            "openid": openid,
        }
        return self._get(self.__refresh_token_url, params=params)

    def get_userinfo(self, access_token, openid, lang="zh_CN"):
        """
        获取用户个人信息（UnionID机制）

        请注意，在用户修改微信头像后，旧的微信头像URL将会失效，因此开发者应该自己在获取用户信
        息后，将头像图片保存下来，避免微信头像URL失效后的异常情况。
        """
        if lang not in ("zh_CN", "zh_TW", "en"):
            return {
                "errcode": "sdk101",
                "errmsg": "invalid param 'lang', should be zh_CN, zh_TW or en",
            }
        params = {
            "access_token": access_token,
            "openid": openid,
            "lang": lang,
        }
        return self._get(self.__check_token_url, params=params)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
