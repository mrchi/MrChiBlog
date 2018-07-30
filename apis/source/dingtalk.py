# coding=utf-8

__author__ = "Invoker"

from .base import APIBase


class DingTalkRobot(APIBase):
    """ 钉钉机器人webhook，发送消息到钉钉群 """

    __robot_webhook_url = "https://oapi.dingtalk.com/robot/send"

    def __init__(self, access_token, at_mobiles=[], is_at_all=False, req=None):
        self._access_token = access_token.strip()
        self.set_at(at_mobiles, is_at_all)
        super().__init__(req=req)

    def set_at(self, at_mobiles=[], is_at_all=False):
        """ 设定是否@群成员 """
        self._is_at_all = bool(is_at_all)
        self._at_mobiles = [] if self._is_at_all else at_mobiles

    def _send(self, msg):
        """ 发送消息 """
        return self._post(
            self.__robot_webhook_url,
            params=dict(access_token=self._access_token),
            json=msg,
        )

    def send_text_msg(self, content):
        """ 发送文本消息 """
        msg = {
            "msgtype": "text",
            "text": {
                "content": content.strip(),
            },
            "at": {
                "atMobiles": self._at_mobiles,
                "isAtAll": self._is_at_all,
            },
        }
        return self._send(msg)

    def send_link_msg(self, title, text, msg_url, pic_url=""):
        """ 发送链接消息 """
        msg = {
            "msgtype": "link",
            "link": {
                "title": title.strip(),
                "text": text.strip(),
                "picUrl": pic_url.strip(),
                "messageUrl": msg_url.strip(),
            }
        }
        return self._send(msg)

    def send_markdown_msg(self, title, text):
        """ 发送markdown消息，text参数为markdown语法格式文本"""
        msg = {
            "msgtype": "markdown",
            "markdown": {
                "title": title.strip(),
                "text": text.strip()
            },
            "at": {
                "atMobiles": self._at_mobiles,
                "isAtAll": self._is_at_all,
            },
        }
        return self._send(msg)

    def send_actioncard_msg(
                self,
                title,
                text,
                *btns,
                vertical_btns=True,     # noqa
                hide_avatar=False,
                single_btn=True
            ):
        """
        发送 ActionCard 消息，包括整体跳转 ActionCard 和独立跳转 ActionCard

        text 支持 markdown，
        btn 传入时是 tuple 的形式，内容为 (title, url)
        """
        # 整体跳转 ActionCard
        if single_btn:
            msg = {
                "actionCard": {
                    "title": title.strip(),
                    "text": text.strip(),
                    "btnOrientation": "0",
                    "hideAvatar": "1" if hide_avatar else "0",
                    "singleTitle": btns[0][0],
                    "singleURL": btns[0][1],
                },
                "msgtype": "actionCard",
            }
        # 独立跳转 ActionCard
        else:
            msg = {
                "actionCard": {
                    "title": title.strip(),
                    "text": text.strip(),
                    "btnOrientation": "0" if vertical_btns else "1",
                    "hideAvatar": "1" if hide_avatar else "0",
                    "btns": [{"title": i[0], "actionURL": i[1]} for i in btns],
                },
                "msgtype": "actionCard",
            }
        return self._send(msg)

    def send_feedcard_msg(self, *links):
        """
        发送 FeedCard 类型消息

        link 传入时是 tuple 的形式，内容为 (title, url)
        """
        msg = {
            "feedCard": {
                "links": [
                    {
                        "title": i[0],
                        "messageURL": i[1],
                        "picURL": i[2],
                    } for i in links
                ],
            },
            "msgtype": "feedCard",
        }
        return self._send(msg)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
