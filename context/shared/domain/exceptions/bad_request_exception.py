from .base_exception import BaseException
from context.shared.domain.constants.error_constants import ErrorConstants


class BadRequestException(BaseException):
    def __init__(self, *args):
        super(BadRequestException, self).__init__(status_code=400, message=ErrorConstants.BAD_REQUEST, *args)