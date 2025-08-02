from enum import Enum

class CommonExceptionMessages(str, Enum):
    INVALID_COMMAND_SUB_CLASS = "{command} must be subclass of ICommand"
    INVALID_QUERY_SUB_CLASS = "{query} must be subclass of IQuery"
    COMMAND_NOT_REGISTERED = "{command_type} not registered in CommandBus"
    QUERY_NOT_REGISTERED = "{query_type} not registered in QueryBus"

    def format(self, **kwargs) -> str:
        return self.value.format(**kwargs)