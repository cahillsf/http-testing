from flask import Flask, jsonify, request, Response, make_response
from flask_cors import CORS
import logging
import pymongo
from pprint import pprint
import sys
import datetime
import os

app = Flask(__name__)
app.config.from_object(__name__)
mongo_client = "mongodb"
base_url = ""
# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app, origins=["http://localhost:8080"], headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin'], supports_credentials=True)

@app.route('/api/testRoute', methods=['GET', 'POST'])
def testRoute():
    print(request.json, file=sys.stderr)
    print(request.args, file=sys.stderr)
    print(request)
    args = request.values
    for key in args:
        print(args.get(key), file=sys.stderr)
        print(args.getlist(key), file=sys.stderr)
    print(os.environ.get('DD_AGENT_HOST'), file=sys.stderr)
    app.logger.info(os.environ.get('DD_AGENT_HOST'))
    print("test route", file=sys.stderr)
    app.logger.info("test route")
    return "OKAY", 200

#local deployment
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

#k8s deployment using gunicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    base_url = "/api"
    mongo_client = "ps-mongo-service"