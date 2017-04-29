from typing import Iterable
from typing import Tuple

from gutenberg.query import get_metadata
from gutenberg.query import get_etexts


def lookup_metadata(etextno: int, fields: Iterable[str]):
    return {field: get_metadata(field, etextno) for field in fields}


def find_texts(query: Tuple[str, str]):
    field, value = query
    return get_etexts(field, value)
