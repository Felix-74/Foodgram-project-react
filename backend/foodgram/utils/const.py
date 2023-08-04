from typing import NamedTuple


class MethodConst(NamedTuple):
    '''
    Константы методов запросов
    '''
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    UPDATE = 'UPDATE'
    PUT = 'PUT'
    PATCH = 'PATCH'
