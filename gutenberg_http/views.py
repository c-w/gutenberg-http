from urllib.parse import quote

from flask import redirect
from flask import request
from flask import jsonify

from gutenberg_http import app
from gutenberg_http import cache
from gutenberg_http import config
from gutenberg_http import errors
from gutenberg_http import logic


@app.route('/')
def index():
    return redirect('{test_page_url}?server={server}'.format(
        test_page_url=config.TEST_PAGE_URL,
        server=quote(request.host)))


@app.route('/texts/<int:text_id>')
@cache.cached(query_string=True)
def metadata(text_id: int):
    include = logic.metadata(text_id, request.args.get('include'))
    return jsonify({'text_id': text_id, 'metadata': include})


@app.route('/texts/<int:text_id>/body')
@cache.cached(query_string=True)
def body(text_id: int):
    fulltext = logic.body(text_id)
    return jsonify({'text_id': text_id, 'body': fulltext})


@app.route('/search/<query>')
def search(query: str):
    results = logic.search(query, request.args.get('include'))
    return jsonify({'texts': results})


@app.errorhandler(errors.InvalidUsage)
def bad_request(exception: errors.InvalidUsage):
    error = {'error': 'invalid_usage', 'message': exception.message}
    return jsonify(error), exception.status_code


@app.errorhandler(Exception)
def on_exception(exception: Exception):
    error = {'error': exception.__class__.__name__, 'message': str(exception)}
    return jsonify(error), getattr(exception, 'status_code', 500)


@app.route('/healthcheck')
def healthcheck():
    return jsonify({
        'db': {
            'freshness': logic.db_freshness(),
        },
    })
