#!/usr/bin/env python

"""htmlproxy.py: HTTP proxy that takes a POST request and appends a JSON Web Token."""

__author__      = "Daniel Mundt"

import time
import datetime
import redis
from flask import Flask
from flask import request, Response
import json
import jwt
import random
import requests
from meinheld import server

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

start_time = datetime.datetime.now()
PROXY_DOMAIN = 'https://reqres.in/'


def increment_hit_counter():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def get_hit_count():
    current_cache = cache.get('hits')
    if current_cache:
        return int(current_cache.decode())
    return 0

def create_jwt_token():
    jwt_secret = 'a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf'
    jwt_token = jwt.encode(
        {
            'iat': datetime.datetime.utcnow(),
            'jti': ''.join([str(random.randint(0, 9)) for i in range(8)]),  # method used by python-oauth2
            'payload': {
                'user': 'testuser',
                'date': datetime.date.today().strftime("%d.%m.%Y")
            }
        },
        jwt_secret,
        algorithm='HS512'
    )
    return jwt_token


@app.route('/<path:path>', methods = ['POST'])
def root(path):
    increment_hit_counter()

    new_headers = {key: value for (key, value) in request.headers if key != 'Host'}
    new_headers['x-my-jwt'] = create_jwt_token()

    response = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, PROXY_DOMAIN),
        headers=new_headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        stream=True)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]

    return Response(response, response.status_code, headers)


@app.route('/status')
def status():
    output_data = {
        'hits': get_hit_count(),
        'uptime': (datetime.datetime.now() - start_time).total_seconds()
    }
    response = app.response_class(
        response=json.dumps(output_data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    server.listen(("0.0.0.0", 5000))
    server.run(app)
