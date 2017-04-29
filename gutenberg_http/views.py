from sanic.request import Request
from sanic.response import json

from gutenberg_http import app
from gutenberg_http.logic import find_texts
from gutenberg_http.logic import lookup_metadata
from gutenberg_http.parameters import parse_fields
from gutenberg_http.parameters import parse_search


@app.route('/texts/<text_id:int>')
async def metadata(request: Request, text_id: int):
    requested_fields = parse_fields(request.args.get('fields'))
    field_values = lookup_metadata(text_id, requested_fields)

    return json({'text_id': text_id, 'metadata': field_values})


@app.route('/search')
async def search(request: Request):
    requested_search = parse_search(request.args.get('q'))
    search_results = find_texts(requested_search)

    return json({'text_ids': search_results})
