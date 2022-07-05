#!/bin/bash

echo "Waiting for pg up"
sleep 5

sanic app.main:app --host=0.0.0.0 --port=8000