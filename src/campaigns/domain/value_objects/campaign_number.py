from shared.domain.value_objects.int_value_object import IntValueObject


class CampaignNumber(IntValueObject):
    """Value object representing a campaign number."""

    def __init__(self, value: int, field_name: str = "campaign number"):
        super().__init__(value, field_name, min_value=1, max_value=50)
