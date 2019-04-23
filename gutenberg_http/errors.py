from typing import Iterable
from typing import Union

StringOrStrings = Union[Iterable[str], str]


class GutenbergException(Exception):
    pass


class InvalidUsage(GutenbergException):
    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code


class UnknownFields(InvalidUsage):
    def __init__(self, unknown: StringOrStrings, known: Iterable[str]) -> None:
        if isinstance(unknown, str):
            message = "The field '%s' is not supported." % unknown
        else:
            message = ('The following fields are not supported: %s.'
                       % ', '.join(unknown))
        message = '%s Supported fields are: %s' % (message, ', '.join(known))
        super().__init__(message)


class NoQuery(InvalidUsage):
    def __init__(self) -> None:
        super().__init__('No query specified.')


class NoQueryValue(InvalidUsage):
    def __init__(self) -> None:
        super().__init__('No query value specified.')


class MisformedQuery(InvalidUsage):
    def __init__(self, query: str) -> None:
        super().__init__(
            "Query '%s' is misformed, should be of format "
            "'{field} {operator} {value}'." % query)


class UnknownQueryOperator(InvalidUsage):
    def __init__(self, unknown: str, known: Iterable[str]) -> None:
        super().__init__(
            "The operator '%s' is not supported. Supported operators are: %s"
            % (unknown, ','.join(known)))
