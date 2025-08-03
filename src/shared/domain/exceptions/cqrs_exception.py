from fastapi import status
from shared.domain.exceptions.common_exception import CommonException
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages


class CqrsException(CommonException):
    """Base class for all CQRS-related exceptions."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, message)

    @staticmethod
    def invalid_query_sub_class(query: str) -> 'CqrsException':
        """Exception raised when a query is not a subclass of IQuery."""
        return CqrsException(CommonExceptionMessages.INVALID_QUERY_SUB_CLASS.format(query=query))

    @staticmethod
    def query_not_registered(query_type: str) -> 'CqrsException':
        """Exception raised when a query is not registered in the query bus."""
        return CqrsException(CommonExceptionMessages.QUERY_NOT_REGISTERED.format(query_type=query_type))

    @staticmethod
    def invalid_command_sub_class(command: str) -> 'CqrsException':
        """Exception raised when a command is not a subclass of ICommand."""
        return CqrsException(CommonExceptionMessages.INVALID_COMMAND_SUB_CLASS.format(command=command))

    @staticmethod
    def command_not_registered(command_type: str) -> 'CqrsException':
        """Exception raised when a command is not registered in the command bus."""
        return CqrsException(CommonExceptionMessages.COMMAND_NOT_REGISTERED.format(command_type=command_type))
