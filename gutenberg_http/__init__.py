from logging import getLogger

from applicationinsights.flask.ext import AppInsights
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

cors = CORS(app)
appinsights = AppInsights(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

import gutenberg_http.views  # noqa
