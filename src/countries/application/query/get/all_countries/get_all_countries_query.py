from shared.domain.cqrs.query.iquery import IQuery


class GetAllCountriesQuery(IQuery):
    """Query to retrieve all countries."""

    @staticmethod
    def create() -> "GetAllCountriesQuery":
        """Factory method to create a GetAllCountriesQuery instance."""
        return GetAllCountriesQuery()
