# coding=utf-8

from urllib.parse import urljoin
import hmac

import requests


class CodingPost:
    def __init__(self, access_token, owner, project, rootdir, commit_sha=None):
        self._access_token = access_token
        self._connect_timeout = 5.0
        self._socket_timeout = 5.0
        self.owner = owner
        self.project = project
        self.rootdir = rootdir
        self.commit_sha = commit_sha or self.get_last_commit()

    def _http_get(self, url, params=None, headers={}, **kw):
        """HTTP GET请求，封装Coding token鉴权和基本错误处理"""
        headers["Authorization"] = f"token {self._access_token}"
        resp = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=(self._connect_timeout, self._socket_timeout),
            **kw,
        )
        data = resp.json()
        return data

    def get_last_commit(self):
        """获取最新提交的sha值"""
        url = f"https://coding.net/api/user/{self.owner}/project/{self.project}/git"
        result = self._http_get(url)
        return result["data"]["depot"]["lastCommitSha"]

    def get_all_files_list(self):
        """获取全量md文件列表，包括子目录中的文件。"""
        base_url = f"https://coding.net/api/user/{self.owner}/project/{self.project}/git/tree/{self.commit_sha}/"
        results = []
        visit_list = [self.rootdir]
        while visit_list:
            url = urljoin(base_url, "./" + visit_list.pop().lstrip("/"))
            result = self._http_get(url)
            for fileinfo in result["data"]["files"]:
                if fileinfo["mode"] == "tree":
                    visit_list.append(fileinfo["path"])
                elif fileinfo["mode"] == "file":
                    results.append(fileinfo["path"])
        return results

    def get_file_content(self, file_path):
        """获取单个文件的标题、内容、最后修改作者和最后修改时间。"""
        base_url = f"https://coding.net/api/user/{self.owner}/project/{self.project}/git/blob/{self.commit_sha}/"
        url = urljoin(base_url, "./" + file_path.lstrip("/"))
        result = self._http_get(url)
        file_data = result["data"]["file"]
        return {
            "title": file_data["name"].strip(".md"),
            "content": file_data["data"],
            "author": file_data["lastCommitter"]["name"],
            "timestamp": file_data["lastCommitDate"],
        }


class CodingSignature:
    @classmethod
    def check_webhook_signature(cls, token, request_data, signature):
        """
        验证 Coding webhook 的签名。

        :param token: 在创建 webhook 时填写的令牌。
        :param request_data: webhook POST 请求内容，可以传入 bytes 或者 str 类型。
        :param signature: webhook POST 请求头中 X-Coding-Signature 字段，通过
        HMAC SHA1 加密算法、使用令牌作为 KEY 将发送内容加密后的值以十六进制显示（需要配置令牌）,并包含前缀 sha1=
        :returns: 签名验证通过返回True，否则返回False。
        """
        if isinstance(token, str):
            token = token.encode()
        if isinstance(request_data, str):
            request_data = request_data.encode()
        if isinstance(signature, bytes):
            signature = signature.decode()
        if signature.startswith("sha1="):
            signature = signature[5:]
        return signature == hmac.new(token, request_data, "sha1").hexdigest()
