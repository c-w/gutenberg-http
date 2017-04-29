from gutenberg.acquire import load_etext
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata

from gutenberg_http.parameters import parse_fields
from gutenberg_http.parameters import parse_search


def metadata(fields: str, text_id: int) -> dict:
    fields = parse_fields(fields)

    metadata_values = {field: get_metadata(field, text_id) for field in fields}

    return {'text_id': text_id, 'metadata': metadata_values}


def body(text_id: int) -> str:
    return load_etext(text_id)


def search(query: str) -> dict:
    conjunction = parse_search(query)

    parts = iter(get_etexts(field, value) for field, value in conjunction)
    results = set(next(parts))
    [results.intersection_update(result_part) for result_part in parts]

    return {'text_ids': results}
