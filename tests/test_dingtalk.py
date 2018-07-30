# coding=utf-8

__author__ = "Invoker"

import unittest
from source.dingtalk import DingTalkRobot


class TestDingTalkRobot(unittest.TestCase):
    def setUp(self):
        access_token = \
            "18bb57ca411b9b38c99b9ced0972dfe8d788918e945b11617e88dc92f60b6046"
        self.robot = DingTalkRobot(access_token=access_token)

    def test_set_at_mobile(self):
        self.robot.set_at(at_mobiles=["19912345678"])
        resp = self.robot.send_text_msg("我要at一个人")

        self.assertEqual(resp, {'errcode': 0, 'errmsg': 'ok'})

    def test_set_at_all(self):
        self.robot.set_at(at_mobiles=["19912345678"], is_at_all=True)
        resp = self.robot.send_text_msg("我要at所有人")

        self.assertEqual(resp, {'errcode': 0, 'errmsg': 'ok'})

    def test_text_msg(self):
        text = "人生苦短\n我用Python"
        resp = self.robot.send_text_msg(text)

        self.assertEqual(resp, {'errcode': 0, 'errmsg': 'ok'})

    def test_link_msg(self):
        title = "Python大法好"
        text = "人生苦短，我用Python，么么哒～～～"
        msg_url = "https://www.python.org/"
        pic_url = "https://www.python.org/static/img/python-logo@2x.png"
        resp = self.robot.send_link_msg(title, text, msg_url, pic_url=pic_url)

        self.assertEqual(resp, {'errcode': 0, 'errmsg': 'ok'})

    def test_markdown_msg(self):
        title = "markdown内容测试"
        text = "\n".join([
            "标题",
            "# 一级标题",
            "## 二级标题",
            "### 三级标题",
            "#### 四级标题",
            "##### 五级标题",
            "###### 六级标题",
            "",
            "引用",
            "> A man who stands for nothing will fall for anything.",
            "",
            "文字加粗、斜体",
            "**bold**",
            "*italic*",
            "",
            "链接",
            "[this is a link](https://www.python.org/)",
            "",
            "图片",
            "![](https://www.python.org/static/img/python-logo@2x.png)",
            "",
            "无序列表",
            "- item1",
            "- item2",
            "",
            "有序列表",
            "1. item1",
            "2. item2",
        ])
        resp = self.robot.send_markdown_msg(title, text)

        self.assertEqual(resp, {'errcode': 0, 'errmsg': 'ok'})

    def test_single_btn_actioncard_msg(self):
        title = "年轻人，请忍受一下"
        text = "![]({imgurl})\n\n{summary}".format(
            imgurl="http://mmbiz.qpic.cn/mmbiz_jpg/Ia6gU9JNtkpJOYCcYuDPJ7LKG1licUtyPwqQ7SFMVXribZnaN5PeBI2f8gVW1jOg59Nx4DzLwQcAFicg2I9hUNHyg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1",
            summary="很久没有在《槽边往事》读过诗了，诗歌一直都有，但读诗的心情却少有。昨天很偶然看到一首诗《年轻人，请忍受一下》，看完之后不由自主地读了一遍，突然就有了读诗的心情。"
        )
        btn = ("阅读全文", "https://mp.weixin.qq.com/s/9xsXNAfYHrt3z7KXTdbj1A")
        resp = self.robot.send_actioncard_msg(
            title,
            text,
            btn,
            hide_avatar=True
        )

        self.assertEqual(resp, {'errcode': 0, 'errmsg': 'ok'})

    def test_multi_btns_actioncard_msg(self):
        title = "Neo的选择"
        text = "![]({imgurl})\n\n{summary}".format(
            imgurl="https://pic2.zhimg.com/50/55151a19593e3a8cf95912622e1f695a_hd.jpg",
            summary="Red pill or blue pill？"
        )
        btns = [
            ("Red pill", "https://m.google.com/"),
            ("Blue pill", "https://m.baidu.com"),
        ]
        resp = self.robot.send_actioncard_msg(
            title,
            text,
            *btns,
            vertical_btns=False,
            single_btn=False
        )

        self.assertEqual(resp, {'errcode': 0, 'errmsg': 'ok'})

    def test_feedcard_msg(self):
        links = [
            (
                "《黑客帝国》中的先知是人还是程序？",
                "https://www.zhihu.com/question/25067926",
                "https://pic1.zhimg.com/90ded5596b1ddbb2ea756daaa14f17bf_400x224.jpg",
            ),
            (
                "《黑客帝国》里的锡安是不是虚拟世界？",
                "https://www.zhihu.com/question/19644847",
                "https://pic2.zhimg.com/50/55151a19593e3a8cf95912622e1f695a_400x224.jpg",
            ),
            (
                "怎么能证明我们是生活在《黑客帝国》中的世界？",
                "https://www.zhihu.com/question/21243171",
                "https://pic1.zhimg.com/4548c07d04673b815976ed8f3154c201_400x224.jpg",
            ),
        ]
        resp = self.robot.send_feedcard_msg(*links)

        self.assertEqual(resp, {'errcode': 0, 'errmsg': 'ok'})
