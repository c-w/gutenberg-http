from typing import List
from typing import Optional

from gutenberg.acquire import load_etext
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata

from gutenberg_http import config
from gutenberg_http.cache import lru_cache_truthy_only
from gutenberg_http.parameters import parse_include
from gutenberg_http.parameters import parse_search


@lru_cache_truthy_only(maxsize=config.METADATA_CACHE_SIZE)
def metadata(text_id: int, include: Optional[str] = None) -> dict:
    fields = parse_include(include)

    metadata_values = {field: get_metadata(field, text_id) for field in fields}

    return metadata_values


@lru_cache_truthy_only(maxsize=config.BODY_CACHE_SIZE)
def body(text_id: int) -> str:
    return load_etext(text_id)


@lru_cache_truthy_only(maxsize=config.SEARCH_CACHE_SIZE)
def search(query: str, include: Optional[str] = None) -> List[dict]:
    fields = parse_include(include) if include else []
    conjunction = parse_search(query)

    parts = iter(get_etexts(field, value) for field, value in conjunction)
    results = set(next(parts))
    [results.intersection_update(part) for part in parts]  # type: ignore

    return [dict([('text_id', text_id)] +
                 [(field, get_metadata(field, text_id)) for field in fields])
            for text_id in results]
