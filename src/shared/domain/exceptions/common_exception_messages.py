from enum import Enum


class CommonExceptionMessages(str, Enum):
    """Common exception messages used across the application."""

    INVALID_COMMAND_SUB_CLASS = "{command} must be subclass of ICommand"
    INVALID_QUERY_SUB_CLASS = "{query} must be subclass of IQuery"
    COMMAND_NOT_REGISTERED = "{command_type} not registered in CommandBus"
    QUERY_NOT_REGISTERED = "{query_type} not registered in QueryBus"
    STRING_VALUE_OBJECT_MUST_BE_STRING = "{string} must be a string"
    STRING_VALUE_OBJECT_CANNOT_BE_EMPTY = "{string} cannot be empty"
    ID_VALUE_OBJECT_MUST_BE_VALID_UUID = "{id} must be a valid UUID V4"
    INT_VALUE_OBJECT_MUST_BE_INTEGER = "{integer} must be an integer"
    INT_VALUE_OBJECT_MIN_VALUE = "{integer} must be greater than or equal to {min_value}"
    INT_VALUE_OBJECT_MAX_VALUE = "{integer} must be less than or equal to {max_value}"
    ENTITY_NOT_FOUND = "{entity} with identifier {id} was not found"

    def format(self, **kwargs) -> str:
        return self.value.format(**kwargs)
