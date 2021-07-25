#!/bin/bash

if [ -z "$1" ]; then
    exec python htmlproxy.py
else
    exec "$@"
fi
