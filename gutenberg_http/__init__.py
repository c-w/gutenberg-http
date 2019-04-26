from applicationinsights.flask.ext import AppInsights
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
AppInsights(app)

import gutenberg_http.views  # noqa
