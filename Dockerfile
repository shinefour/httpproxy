FROM python:3.7
MAINTAINER Daniel Mundt "post@danielmundt.de"

ENV FLASK_APP=httpproxy.py
ENV FLASK_RUN_HOST=0.0.0.0
#ENV FLASK_ENV=development
EXPOSE 5000

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["flask", "run"]
