# coding=utf-8

# 参考以下配置示例
# https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
# http://docs.gunicorn.org/en/stable/settings.html#settings

from multiprocessing import cpu_count

bind = ["127.0.0.1:5000", "unix:/tmp/mrchiblog.sock"]   # 绑定监听地址
backlog = 2048                  # pending状态的最大连接数

workers = cpu_count() * 2 + 1   # worker进程数量，推荐值 CPU数量*2+1
worker_class = "sync"           # worker 工作模式
threads = 2                     # 每个worker进程的线程数，推荐值范围 [2, 4*cpu数量]
timeout = 30                    # worker进程超时时间，超时后会重启或杀掉进程

accesslog = "-"                 # 访问日志输出到 stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

errorlog = "-"                  # 错误日志输出到 stderr
loglevel = "info"               # 错误日志级别
