from gutenberg.acquire import load_etext
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata
from sanic.request import Request
from sanic.response import json
from sanic.response import text

from gutenberg_http import app
from gutenberg_http.parameters import parse_fields
from gutenberg_http.parameters import parse_search


@app.route('/texts/<text_id:int>')
async def metadata(request: Request, text_id: int):
    fields = parse_fields(request.args.get('fields'))
    metadata_values = {field: get_metadata(field, text_id) for field in fields}

    return json({'text_id': text_id, 'metadata': metadata_values})


# noinspection PyUnusedLocal
@app.route('/texts/<text_id:int>/body')
async def body(request: Request, text_id: int):
    body_value = load_etext(text_id)

    return text(body_value)


# noinspection PyUnusedLocal
@app.route('/search/<query>')
async def search(request: Request, query: str):
    field, value = parse_search(query)
    search_results = get_etexts(field, value)

    return json({'text_ids': search_results})
