from sanic import Sanic

app = Sanic(__name__)

import gutenberg_http.views  # noqa
