from pymongo import MongoClient


class MongoDBConnection:
    """MongoDB connection manager class."""

    def __init__(self, uri: str, db_name: str):
        self._client = MongoClient(uri)
        self._db = self._client[db_name]

    @property
    def client(self):
        return self._client

    @property
    def db(self):
        return self._db
