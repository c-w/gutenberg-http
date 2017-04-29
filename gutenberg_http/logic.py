from gutenberg.acquire import load_etext
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata

from gutenberg_http import config
from gutenberg_http.cache import lru_cache_truthy_only
from gutenberg_http.parameters import parse_fields
from gutenberg_http.parameters import parse_search


@lru_cache_truthy_only(maxsize=config.METADATA_CACHE_SIZE)
def metadata(fields: str, text_id: int) -> dict:
    fields = parse_fields(fields)

    metadata_values = {field: get_metadata(field, text_id) for field in fields}

    return metadata_values


@lru_cache_truthy_only(maxsize=config.METADATA_CACHE_SIZE)
def body(text_id: int) -> str:
    return load_etext(text_id)


@lru_cache_truthy_only(maxsize=config.METADATA_CACHE_SIZE)
def search(query: str) -> set:
    conjunction = parse_search(query)

    parts = iter(get_etexts(field, value) for field, value in conjunction)
    results = set(next(parts))
    [results.intersection_update(part) for part in parts]  # type: ignore

    return results
