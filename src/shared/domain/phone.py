from shared.domain.value_objects.common.country_phone_code import CountryPhoneCode
from shared.domain.value_objects.common.phone_number import PhoneNumber
from shared.domain.value_objects.phone_dict import PhoneDict


class Phone:

    def __init__(self, country_code: CountryPhoneCode, number: PhoneNumber):
        """
        :param country_code: The country phone code.
        :param number: The phone number.
        """
        self.country_code = country_code
        self.number = number

    def to_dict(self) -> PhoneDict:
        """
        Converts the Phone object to a dictionary representation.

        :return: A dictionary with country code and phone number.
        """
        return PhoneDict(
            country_code=self.country_code.int,
            number=self.number.int
        )

    @classmethod
    def from_dict(cls, phone_dict: PhoneDict) -> "Phone":
        """
        Creates a Phone instance from a dictionary representation.
        :param phone_dict: A dictionary containing country code and phone number.
        """
        return cls(
            country_code=CountryPhoneCode(phone_dict["country_code"]),
            number=PhoneNumber(phone_dict["number"])
        )
