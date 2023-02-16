FROM python:3.8.5-alpine

LABEL maintainer="Shashank Aital"

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev supervisor openssh

RUN mkdir /code
RUN mkdir /mounts
RUN mkdir /var/log/supervisord

WORKDIR /code

COPY requirements.txt /code/
COPY supervisord/supervisord.conf /etc/supervisord.conf

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
