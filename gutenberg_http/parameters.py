from typing import Optional

from gutenberg.query import list_supported_metadatas

from gutenberg_http.errors import MisformedQuery
from gutenberg_http.errors import NoQuery
from gutenberg_http.errors import NoQueryValue
from gutenberg_http.errors import UnknownFields
from gutenberg_http.errors import UnknownQueryOperator

ALL_FIELDS = frozenset(list_supported_metadatas())

ALL_OPERATORS = frozenset({'eq'})


def parse_fields(query: Optional[str]):
    if not query:
        return ALL_FIELDS

    requested_fields = set(query.split(','))
    unknown_fields = requested_fields - ALL_FIELDS
    if unknown_fields:
        raise UnknownFields(unknown_fields, ALL_FIELDS)

    return requested_fields


def parse_search(query: Optional[str]):
    if not query:
        raise NoQuery()

    try:
        field, operation, *values = [_.strip() for _ in query.split(' ')]
    except ValueError:
        raise MisformedQuery(query)

    if operation not in ALL_OPERATORS:
        raise UnknownQueryOperator(operation, ALL_OPERATORS)

    if field not in ALL_FIELDS:
        raise UnknownFields(field, ALL_FIELDS)

    value = ' '.join(values)
    if not value:
        raise NoQueryValue()

    return field, value
