FROM python:3.6-slim
MAINTAINER Daniel Mundt "post@danielmundt.de"

COPY . /app
WORKDIR /app

ENV FLASK_APP=httpproxy.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

RUN python -m pip install -r requirements.txt
CMD ["flask", "run"]
