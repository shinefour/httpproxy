#!/usr/bin/env python
"""htmlproxy.py: HTTP proxy that takes a POST request and appends a JSON Web Token."""

__author__ = "Daniel Mundt"

from flask import Flask
from flask import request, Response
import requests
from meinheld import server
import base64
import json

app = Flask(__name__)


def create_opt_data():
    opt_data = {
        'userId': 'purchase',
        'merchant': '###merchant###',
        'sessionId': 'proxy'
    }
    return str(base64.urlsafe_b64encode(json.dumps(opt_data).encode()).decode())


@app.route('/<path:drm_system>', methods=['POST', 'OPTIONS'])
def root(drm_system):
    new_headers = {key: value for (key, value) in request.headers}
    new_headers['x-dt-custom-data'] = create_opt_data()

    if drm_system == 'Widevine':
        url = 'https://lic.staging.drmtoday.com/license-proxy-widevine/cenc/?specConform=true'
    elif drm_system == 'FairPlay':
        url = 'https://lic.staging.drmtoday.com/license-proxy-headerauth/drmtoday/RightsManager.asmx'
    elif drm_system == 'PlayReady':
        url = 'https://lic.staging.drmtoday.com/license-server-fairplay/'
    else:
        raise Exception("Invalid drm system (one of: Widevine, PlayReady, FairPlay)")

    response = requests.request(
        method=request.method,
        url=url,
        headers=new_headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        stream=False)

    # excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    # headers = [(name, value) for (name, value) in response.raw.headers.items()
    #            if name.lower() not in excluded_headers]

    return Response(response.content, status=response.status_code, headers=dict(response.headers))


if __name__ == '__main__':
    server.listen(("0.0.0.0", 5000))
    server.run(app)
