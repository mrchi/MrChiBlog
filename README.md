# MrChiBlog
使用 Flask 和 Bootstrap 构建的轻量博客，基于 Git 存储博客内容（目前支持 Coding.net）。

项目缘起于在前司工作期间，需要搭建一个团队技术博客，需要支持团队多人发布文章，并放在公网访问。彼时团队代码托管在 Coding，刚好也不想增加新的一套账号体系，因此想到了 Coding repo 作为文章来源，使用 Coding API 来获取内容并展示的方案。不巧的是，在职期间一直没时间实现，离职后终于动手实现了基本功能。

曾在某公众号（冯大辉或者和菜头，记不清了）的推文中看到过说，做事分为两个阶段：从零到一，从一到多。从零到一是创造，从一到多是优化迭代。这个项目陆陆续续写了大概两个月，却也仅仅是几个静态页面模版罢了。优化迭代是一个循序渐进、不断重构的过程，对于这个项目，这才刚开始，后续任重而道远。

# 特性

- 使用 Git（目前支持 Coding 托管）管理 markdown 文章，支持扩展 markdown 语法；
- 通过 Coding webhook 自动更新文章内容；
- 支持文章拥有以下元数据：作者、分类（一个）、标签（多个）和创建时间；
- 支持按分类和标签查看文章；
- 支持全文检索文章标题和内容；
- 支持自动生成文章目录，并显示当前阅读位置；
- Docker 快速部署；
- 通过钉钉接收 HTTP 500 告警；

# 使用的技术和库

## 前端

- Bootstrap
- jQuery
- Moment.js
- Font Awesome

## 后端

- Flask
- Celery
- Gunicorn
- Flask-SQLAlchemy
- Flask-WhooshAlchemyPlus
- Whoosh
- Jieba
- python-markdown
- Pygments
- requests
- PyMySQL

# 使用方法

## 普通部署

安装 redis、rabbitmq 和 mysql，并创建 mysql 数据库（建议使用 utf8mb4 编码以兼容 emoji 表情等字符）。

拉取代码：

```
git clone https://github.com/chiqj/MrChiBlog.git
```

安装依赖：

```
cd MrChiBlog
pipenv install --deploy
```

在项目根目录创建 `.env` 环境变量文件，示例如下：

```
# 生产环境 mysql 数据库
PROD_DATABASE_URI=mysql+pymysql://test:test123@127.0.0.1:3306/mrchiblog?charset=utf8mb4

# 指定 Flask app
FLASK_APP=manage:app
# 指定 Flask 在 production 模式
FLASK_ENV=production

# Coding 仓库配置，依次为 所有者用户名、仓库名、文章在仓库中的父目录
OWNER=user
PROJECT=repo
ROOTDIR=/

# Coding Access Token，用于 Coding API 请求数据，注意设置权限
ACCESS_TOKEN=1234567890

# Coding 该 repo 的 webhook token，用于接收 PR 和 commit 消息，触发更新
WEBHOOK_TOKEN=1234567890

# 生成文章固定链接的密钥
HMAC_KEY=foobar

# 钉钉 robot token，用于接收 HTTP 500 消息
PROD_DINGTALK_TOKEN=123456789000000

# 生产环境 redis 数据库
PROD_REDIS_URI=redis://127.0.0.1:6379/0

# 生产环境 whoosh 索引目录配置
PROD_WHOOSH_BASE=./prod_whoosh_idx

# Celery 配置
CELERY_BROKER_URL=amqp://127.0.0.1:5672
CELERY_RESULT_BACKEND=disabled
```

初始化数据库：

```
pipenv run flask deploy
```

运行：

```
pipenv run gunicorn -c gunicorn.py -b 0.0.0.0:5000 manage:app
```

启动 celery 任务：

```
pipenv run celery worker -A manage:celery_update -l info -n celery-update
pipenv run celery worker -A manage:celery_notify -l info -n celery-notify
```

访问 `5000` 端口即可。

## Docker 部署

拉取代码：

```
git clone https://github.com/chiqj/MrChiBlog.git
```

在项目根目录创建 `.env` 环境变量文件。与普通部署时略有不同:

- 需要分别指定 mysql 数据库用户名、密码、数据库名；
- redis 和 rabbitmq url 中的主机部分都使用容器名。

示例如下：

```
# 生产环境 mysql 数据库
MYSQL_USER=test
MYSQL_PASSWORD=test123
MYSQL_DATABASE=mrchiblog

# 指定 Flask app
FLASK_APP=manage:app
# 指定 Flask 在 production 模式
FLASK_ENV=production

# Coding 仓库配置，依次为 所有者用户名、仓库名、文章在仓库中的父目录
OWNER=user
PROJECT=repo
ROOTDIR=/

# Coding Access Token，用于 Coding API 请求数据，注意设置权限
ACCESS_TOKEN=1234567890

# Coding 该 repo 的 webhook token，用于接收 PR 和 commit 消息，触发更新
WEBHOOK_TOKEN=1234567890

# 生成文章固定链接的密钥
HMAC_KEY=foobar

# 钉钉 robot token，用于接收 HTTP 500 消息
PROD_DINGTALK_TOKEN=123456789000000

# 生产环境 redis 数据库
PROD_REDIS_URI=redis://redis:6379/0

# 生产环境 whoosh 索引目录配置
PROD_WHOOSH_BASE=./prod_whoosh_idx

# Celery 配置
CELERY_BROKER_URL=amqp://rabbitmq:5672
CELERY_RESULT_BACKEND=disabled
```

然后

```
docker-compose build
docker-compose up -d
```

初始化数据库：

```
docker exec -it mrchiblog_web_1 flask deploy
```

在宿主机上访问 `127.0.0.1:5000` 即可。

## 在 markdown 中包含元数据

目前我是将一些元数据直接放到了 markdown 文档中， [python-markdown](https://python-markdown.github.io/) 库在转换为 html 时，通过 [Meta-data](https://python-markdown.github.io/extensions/meta_data/) 扩展读取这些元数据并存入数据库，而转换得到的 html 中不会包含这些元数据。这种方式，无疑给写文档的人增加了一定工作量，但好处是，所有信息都在 Coding repo 中，任何时候都可以删库重建而不会造成数据丢失。

在 markdown 中包含的元数据包括：分类（category）、标签（labels）和创建时间（create_at）。示例如下：

```markdown
---
category: Docker
labels: Docker
        Dockerfile
create_at: 2018-08-10 17:40:45
---

这是 markdown 正文第一句话。Good luck, have fun.
```

元数据写在 markdown 文档的开头，以 `---` 行开头（L1）和结尾（L6），并与 markdown 正文之间有一个空行（上面的 L7）。元数据采用 yaml 语法，分类和创建时间只能有一个，标签可以有多个。多个标签分别写在不同行，并保证从第二个标签开始，缩进大于 2 个空格。

上面的示例中，该文章分类为 “Docker”，标签为 “Docker” 和 “Dockerfile”，创建时间为 “2018-08-10 17:40:45”。

# 开发

开发时，Flask 应被设置为 development 模式。相比普通部署的 `.env` 文件，部分环境变量需要调整，包括：

```
# flask 应用工作在 development 模式，开启 debug 和 auto_reload
FLASK_ENV = "development"

# 开发环境 mysql 数据库
DEV_DATABASE_URI

# 开发环境 redis 数据库
DEV_REDIS_URI

# 开发环境 whoosh 索引目录
DEV_WHOOSH_BASE

# 开发环境 dingtalk robot token
DEV_DINGTALK_TOKEN
```

初始化：

```
flask deploy
```

运行：

```
flask run
```

访问 `http://127.0.0.1:5000` 即可。

# 感谢

- 感谢前司“学长”的技术指导，在 Docker 方面帮助了我很多。
- 感谢不愿透露姓名的“菜鸡”同学帮我解决前端bug。
- 由于我前端水平不够高，博客页面样式和配色大量借鉴了 [SegmentFault](https://segmentfault.com/)，在此对 SegmentFault 表示感谢。如果 SegmentFault 觉得我侵犯了您的利益，请与我联系。

# Todo

1. 增加测试用例并实现 TDD；
2. 使用“操作 Git 仓库”方式替代“使用 Coding API”方式获得内容和数据（可兼容任意 Git 托管平台）；
3. 文章支持多作者，并增加按作者展示文章内容；
4. 增加后台管理；
5. 增加评论；
6. 前后端分离 + Restful 接口；