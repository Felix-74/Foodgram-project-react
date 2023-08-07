from typing import NamedTuple


class MethodConst(NamedTuple):
    """
    Константы методов запросов
    """
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    UPDATE = 'UPDATE'
    PUT = 'PUT'
    PATCH = 'PATCH'

class IntConst(NamedTuple):
    """
    Константы инт
    """
    MIN_SMALL = 1
    MAX_SMALL = 32000