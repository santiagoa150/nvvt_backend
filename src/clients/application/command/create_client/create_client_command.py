from typing import Optional

from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.common.country_phone_code import CountryPhoneCode
from shared.domain.value_objects.common.phone_number import PhoneNumber
from shared.domain.value_objects.string_value_object import StringValueObject


class CreateClientCommand(ICommand):
    """Command to create a new client."""

    def __init__(
            self,
            given_names: StringValueObject,
            family_names: Optional[StringValueObject],
            delivery_place: StringValueObject,
            phone_number: Optional[PhoneNumber],
            country_phone_code: Optional[CountryPhoneCode],
    ):
        """
        :param given_names: The given names of the client.
        :param family_names: The family names of the client.
        :param delivery_place: The delivery place of the client.
        :param phone_number: The phone number of the client.
        :param country_phone_code: The country phone code of the client.
        """
        self.given_names = given_names
        self.family_names = family_names
        self.delivery_place = delivery_place
        self.phone_number = phone_number
        self.country_phone_code = country_phone_code
