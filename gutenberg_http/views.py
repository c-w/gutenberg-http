from datetime import datetime
from datetime import timezone
from os.path import getmtime
from urllib.parse import quote

from sanic.exceptions import RequestTimeout
from sanic.request import Request
from sanic.response import json
from sanic.response import redirect

from gutenberg_http import app
from gutenberg_http import config
from gutenberg_http.errors import InvalidUsage
from gutenberg_http.logic import body as _body
from gutenberg_http.logic import metadata as _metadata
from gutenberg_http.logic import search as _search


@app.route('/')
async def index(request: Request):
    return redirect('{test_page_url}?server={server}'.format(
        test_page_url=config.TEST_PAGE_URL,
        server=quote(request.scheme + '://' + request.host)))


@app.route('/texts/<text_id:int>')
async def metadata(request: Request, text_id: int):
    include = _metadata(text_id, request.args.get('include'))
    return json({'text_id': text_id, 'metadata': include})


# noinspection PyUnusedLocal
@app.route('/texts/<text_id:int>/body')
async def body(request: Request, text_id: int):
    fulltext = _body(text_id)
    return json({'text_id': text_id, 'body': fulltext})


# noinspection PyUnusedLocal
@app.route('/search/<query>')
async def search(request: Request, query: str):
    results = _search(query, request.args.get('include'))
    return json({'texts': results})


# noinspection PyUnusedLocal
@app.exception(InvalidUsage)
async def bad_request(request: Request, exception: InvalidUsage):
    error = {'error': 'invalid_usage', 'message': exception.message}
    return json(error, exception.status_code)


# noinspection PyUnusedLocal
@app.exception(RequestTimeout)
async def timeout(request: Request, exception: RequestTimeout):
    error = {'error': 'timeout', 'message': 'The request timed out.'}
    return json(error, exception.status_code)


# noinspection PyUnusedLocal
@app.exception(Exception)
async def on_exception(request: Request, exception: Exception):
    error = {'error': exception.__class__.__name__, 'message': str(exception)}
    return json(error, getattr(exception, 'status_code', 500))


# noinspection PyUnusedLocal,PyProtectedMember
@app.route('/healthcheck')
async def healthcheck(request: Request):
    try:
        db_freshness = str(datetime.fromtimestamp(
            getmtime(config.DB_DIR), timezone.utc))
    except (FileNotFoundError, TypeError):
        db_freshness = None

    return json({
        'db': {
            'freshness': db_freshness,
        },
        'caches': {
            'metadata': _metadata.cache_info()._asdict(),
            'body': _body.cache_info()._asdict(),
            'search': _search.cache_info()._asdict(),
        }
    })
