#!/usr/bin/env python

"""htmlproxy.py: HTTP proxy that takes a POST request and appends a JSON Web Token."""

__author__      = "Daniel Mundt"

import time
import datetime
import redis
from flask import Flask
import json

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

start_time = datetime.datetime.now()

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
        return current_cache.decode()
    return 0

@app.route('/')
def root():
    return str(increment_hit_counter())

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

