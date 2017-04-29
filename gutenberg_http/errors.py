from typing import Iterable
from typing import Union

from sanic.exceptions import InvalidUsage

StringOrStrings = Union[Iterable[str], str]


class UnknownFields(InvalidUsage):
    def __init__(self, unknown: StringOrStrings, known: Iterable[str]):
        if isinstance(unknown, str):
            message = 'The field "%s" is not supported.' % unknown
        else:
            message = ('The following fields are not supported: %s.'
                       % ', '.join(unknown))
        message = '%s Supported fields are: %s' % (message, ', '.join(known))
        super().__init__(message)


class NoQuery(InvalidUsage):
    def __init__(self):
        super().__init__('No query specified.')


class NoQueryValue(InvalidUsage):
    def __init__(self):
        super().__init__('No query value specified.')


class MisformedQuery(InvalidUsage):
    def __init__(self, query):
        super().__init__(
            'Query "%s" is misformed, should be of format '
            '"{field} {operator} {value}".' % query)


class UnknownQueryOperator(InvalidUsage):
    def __init__(self, unknown: str, known: Iterable[str]):
        super().__init__(
            'The operator "%s" is not supported. Supported operators are: %s'
            % (unknown, ','.join(known)))
