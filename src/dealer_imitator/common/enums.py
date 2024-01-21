from enum import Enum, StrEnum


class Games(StrEnum):
    BLACKJACK = "blackjack"
    CASINO_POKER = "casino_poker"
    BACCARAT = "baccarat"


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
