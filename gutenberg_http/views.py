from sanic.request import Request
from sanic.response import json
from sanic.response import text

from gutenberg_http import app
from gutenberg_http import logic
from gutenberg_http.errors import InvalidUsage


@app.route('/texts/<text_id:int>')
async def metadata(request: Request, text_id: int):
    return json(logic.metadata(request.args.get('fields'), text_id))


# noinspection PyUnusedLocal
@app.route('/texts/<text_id:int>/body')
async def body(request: Request, text_id: int):
    return text(logic.body(text_id))


# noinspection PyUnusedLocal
@app.route('/search/<query>')
async def search(request: Request, query: str):
    return json(logic.search(query))


# noinspection PyUnusedLocal
@app.exception(InvalidUsage)
async def bad_request(request: Request, exception: InvalidUsage):
    error = {'error': 'invalid_usage', 'message': exception.message}
    return json(error, exception.status_code)
