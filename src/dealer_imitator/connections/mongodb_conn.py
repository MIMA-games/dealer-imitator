import motor.motor_asyncio

from dealer_imitator.common.utils import singleton, mongo_converter, get_timestamp


@singleton
class Mongodb:
    """
    Singleton class for handiling mongodb connection,
    creating indexes, inserting data and querying information.
    """

    def __init__(self):
        self._client: motor.motor_asyncio.AsyncIOMotorClient
        self._db: motor.motor_asyncio.AsyncIOMotorDatabase

    async def connect(
        self,
        db_url: str = "mongodb://localhost:27017",
        db_name: str = "dealer-imitator",
    ):
        """Method for connection to database"""
        self._client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
        self._db = self._client[db_name]

    @property
    def game(self):
        return self._db.game

    @property
    def round(self):
        return self._db.round


db = Mongodb()
