from typing import Any


class CommonException(Exception):
    """Base exception class for all exceptions in this project."""

    def __init__(self, code: int, message: str, detail: Any | None = None):
        self.code = code
        self.message = message
        self.detail = detail

    def __str__(self):
        return f'''
            code: {self.code}
            message: {self.message}
            detail: {self.detail}
            traceback: {self.__traceback__}
            '''

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'detail': self.detail,
        }
