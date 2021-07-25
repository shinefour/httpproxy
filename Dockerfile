FROM python:3.6-slim
MAINTAINER Daniel Mundt "post@danielmundt.de"

COPY . /app
WORKDIR /app

RUN python -m pip install -r requirements.txt

ENTRYPOINT /app/entrypoint.sh