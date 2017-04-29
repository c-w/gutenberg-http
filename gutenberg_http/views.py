from sanic.exceptions import RequestTimeout
from sanic.request import Request
from sanic.response import json
from sanic.response import text

from gutenberg_http import app
from gutenberg_http import logic
from gutenberg_http.errors import InvalidUsage


@app.route('/texts/<text_id:int>')
def metadata(request: Request, text_id: int):
    return json(logic.metadata(request.args.get('fields'), text_id))


# noinspection PyUnusedLocal
@app.route('/texts/<text_id:int>/body')
def body(request: Request, text_id: int):
    return text(logic.body(text_id))


# noinspection PyUnusedLocal
@app.route('/search/<query>')
def search(request: Request, query: str):
    return json(logic.search(query))


# noinspection PyUnusedLocal
@app.exception(InvalidUsage)
def bad_request(request: Request, exception: InvalidUsage):
    error = {'error': 'invalid_usage', 'message': exception.message}
    return json(error, exception.status_code)


# noinspection PyUnusedLocal
@app.exception(RequestTimeout)
def timeout(request: Request, exception: RequestTimeout):
    error = {'error': 'timeout', 'message': 'The request timed out.'}
    return json(error, exception.status_code)
