from shared.domain.value_objects.int_value_object import IntValueObject


class CampaignNumber(IntValueObject):
    """Value object representing a campaign number."""

    def __init__(self, value: int):
        super().__init__(value, "campaign number", min_value=1, max_value=50)
