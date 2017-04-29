from sanic.exceptions import RequestTimeout
from sanic.request import Request
from sanic.response import json
from sanic.response import text

from gutenberg_http import app
from gutenberg_http import logic
from gutenberg_http.errors import InvalidUsage


@app.route('/texts/<text_id:int>')
def metadata(request: Request, text_id: int):
    fields = logic.metadata(request.args.get('fields'), text_id)
    return json({'text_id': text_id, 'metadata': fields})


# noinspection PyUnusedLocal
@app.route('/texts/<text_id:int>/body')
def body(request: Request, text_id: int):
    fulltext = logic.body(text_id)
    return text(fulltext)


# noinspection PyUnusedLocal
@app.route('/search/<query>')
def search(request: Request, query: str):
    results = logic.search(query)
    return json({'text_ids': results})


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
