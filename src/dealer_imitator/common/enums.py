from enum import Enum

class GameStates(Enum):

    CLOSED = "closed"
    PRECOUNTDOWN = "precountdown"
    BETTING = "betting"
    CLOSING_BETS = "closing_bets"
    DEALING = "dealing"
    ANNOUNCING = "announcing"
    SHUFFLING = "shuffling"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
