FROM python:3.7

LABEL name="MrchiBlog"
LABEL description="A simple blog, powered by Flask, Bootstrap and Git."
LABEL maintainer="chiqingjun@gmail.com"

RUN pip install --no-cache-dir pipenv

WORKDIR /mrchiblog

COPY Pipfile Pipfile.lock /mrchiblog/
RUN pipenv install --system --deploy

COPY blog /mrchiblog/blog
COPY *.py README.md /mrchiblog/
RUN mkdir /mrchiblog/logs
