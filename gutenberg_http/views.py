from gutenberg.query import get_etexts
from gutenberg.query import get_metadata
from sanic.request import Request
from sanic.response import json

from gutenberg_http import app
from gutenberg_http.parameters import parse_fields
from gutenberg_http.parameters import parse_search


@app.route('/texts/<text_id:int>')
async def metadata(request: Request, text_id: int):
    fields = parse_fields(request.args.get('fields'))
    field_values = {field: get_metadata(field, text_id) for field in fields}

    return json({'text_id': text_id, 'metadata': field_values})


@app.route('/search')
async def search(request: Request):
    field, value = parse_search(request.args.get('q'))
    search_results = get_etexts(field, value)

    return json({'text_ids': search_results})
