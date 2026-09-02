from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject
from shared.domain.value_objects.str_value_object import StringValueObject


class CartItem:
    """Represents a single line item within a provider's shopping cart."""

    __slots__ = ("_code", "_quantity")

    def __init__(self, code: StringValueObject, quantity: PositiveIntValueObject):
        self._code = code
        self._quantity = quantity

    @property
    def code(self) -> StringValueObject:
        return self._code

    @property
    def quantity(self) -> PositiveIntValueObject:
        return self._quantity
