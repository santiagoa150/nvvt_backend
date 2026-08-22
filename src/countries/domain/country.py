from countries.domain.country_dict import CountryDict
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject
from shared.domain.value_objects.str_value_object import StringValueObject


class Country:
    """Represents a country and its phone dialing code."""

    __slots__ = ("_country_code", "_country_name", "_phone_code")

    def __init__(
        self,
        country_code: StringValueObject,
        country_name: StringValueObject,
        phone_code: PositiveIntValueObject,
    ):
        self._country_code = country_code
        self._country_name = country_name
        self._phone_code = phone_code

    @property
    def country_code(self) -> StringValueObject:
        return self._country_code

    @property
    def country_name(self) -> StringValueObject:
        return self._country_name

    @property
    def phone_code(self) -> PositiveIntValueObject:
        return self._phone_code

    def to_dict(self) -> CountryDict:
        """Converts the country to a dictionary representation."""
        return CountryDict(
            country_code=self._country_code.str,
            country_name=self._country_name.str,
            phone_code=self._phone_code.int,
        )

    @classmethod
    def from_dict(cls, country_dict: CountryDict) -> "Country":
        """Creates a Country instance from a dictionary representation."""
        return cls(
            country_code=StringValueObject(country_dict["country_code"], "country_code"),
            country_name=StringValueObject(country_dict["country_name"], "country_name"),
            phone_code=PositiveIntValueObject(country_dict["phone_code"], "phone_code"),
        )
