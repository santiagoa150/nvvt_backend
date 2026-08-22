from typing import Any, Optional


class CommonException(Exception):
    """Base exception class for all exceptions in this project."""

    def __init__(
        self,
        code: int,
        message: str,
        detail: Any | None = None,
        error_code: Optional[str] = None,
    ):
        self.code = code
        self.message = message
        self.detail = detail
        self.error_code = error_code

    def __str__(self):
        return f"""
            code: {self.code}
            message: {self.message}
            detail: {self.detail}
            error_code: {self.error_code}
            traceback: {self.__traceback__}
            """

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "detail": self.detail,
            "error_code": self.error_code,
        }
