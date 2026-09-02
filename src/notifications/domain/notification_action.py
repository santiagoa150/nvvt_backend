from enum import Enum


class NotificationAction(str, Enum):
    """Enumerates the known notification actions sent by the backend."""

    CART_LOADED = "CART_LOADED"
    CART_LOAD_FAILED = "CART_LOAD_FAILED"
